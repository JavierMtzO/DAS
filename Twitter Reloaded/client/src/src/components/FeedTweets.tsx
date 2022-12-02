import React from "react";
import Tweet from "./Tweet/Tweet";

type Props = {
    title: string,
    tweets: any,
  }

export default function Tweets({title, tweets}: Props)  {
    return (
        <div className="container-fluid h-100 bg-light">
            <div className="d-flex justify-content-center p-4">
                <h3 style={{fontWeight:"700",}}>{title}</h3>
            </div>
            { tweets ? 
                <div>
                {
                    tweets.map(function(tweet){
                    return <Tweet username={tweet['user_id']} message={tweet['content']} date={tweet['timestamp']['$date']}/>   
                    })
                }
                </div>
                :
                <div> </div>
            }  
            {/* <Post/> */}
        </div>
    );
}