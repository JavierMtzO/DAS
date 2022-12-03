import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime

st.set_page_config(layout="wide")

@st.experimental_singleton
def init_connection():
    return MongoClient("mongodb+srv://Gustavo:kUbunriOkGpWyAkT@cluster0.r0fukzf.mongodb.net/?retryWrites=true&w=majority")

mongo = init_connection()

@st.experimental_memo(ttl=600)
def get_data():
    db = mongo['Twitter_Reloaded']
    events = db.events.find()
    events = list(events)
    tweets = db.tweets.find()
    tweets = list(tweets)
    return events, tweets

events, tweets = get_data()

events_list = []
tweets_list = []

for event in events:
    events_list.append({
        "type": event['type'],
        "user": event['user'],
        "timestamp": event['timestamp']
    })

for tweet in tweets:
    res_count = 0
    if 'responses' in tweet:
        for response in tweet['responses']:
            res_count += 1
    tweets_list.append({
        "tweet_id": tweet["_id"],
        "responses": res_count
    })

events_df = pd.DataFrame(events_list)
events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])

tweets_df = pd.DataFrame(tweets_list)

st.title("Event Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Most Recent Activity:")
    st.write(events_df.head(10))
    most_active = events_df.groupby("user")[["timestamp"]].count().head(5)
    st.subheader("Users who Registered the Most Events:")
    most_active = most_active.rename(columns={'timestamp':'events'})
    st.write(most_active)
    fig, ax = plt.subplots()
    ax.bar(most_active.index, most_active['events'])
    plt.title("Most Active Users")
    plt.ylabel("Number of Events")
    st.pyplot(fig)

with col2:
    today = datetime.now().date()
    daily_users = events_df[events_df['timestamp'].dt.date == today].drop_duplicates(
        subset=['user'])['user'].reset_index(drop=True)

    st.subheader("Total Daily Users: " + str(daily_users.count()))
    st.write(daily_users)

    most_responses = tweets_df.sort_values(by=['responses'], ascending=False).head(10)
    st.subheader("Tweets with the Most Replies:")
    st.write(most_responses)
    fig, ax = plt.subplots()
    ax.bar(most_responses['tweet_id'], most_responses['responses'])
    plt.title("Most Replied To Tweets")
    plt.ylabel("Number of Replies")
    plt.xticks(rotation = 45)
    st.pyplot(fig)
