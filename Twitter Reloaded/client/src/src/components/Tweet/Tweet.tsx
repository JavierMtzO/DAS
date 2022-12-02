import React from "react"
import './tweet.css'

type Props = {
  username: string,
  message: string,
  date: string
}

export default function Tweet({username, message, date}: Props) {
    return (   

    <div className="tweet-wrap">
        <link href="https://fonts.googleapis.com/css?family=Asap" rel="stylesheet"/>
        <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet"/>
        <div className="tweet-header">
            <div className="tweet-header-info">
                {username} <span>{username}</span> <span>{date}
                </span>
                <p>{message}</p>        
            </div>    
        </div>
        <div className="tweet-info-counts">    
            <div className="comments">            
                <button style={{backgroundColor:"transparent", border:0}}><svg className="feather feather-message-circle sc-dnqmqq jxshSx" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style={{marginRight: 0}}><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg></button>
                <div className="comment-count">33</div>
            </div>
        </div>
    </div>

    );
}