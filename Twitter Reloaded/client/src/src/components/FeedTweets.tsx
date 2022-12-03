import React from "react";
import Tweet from "./Tweet/Tweet";

type Props = {
    title: string,
    tweets: any
  }

export default function Tweets({title, tweets}: Props)  {
    return (
        <div className="container-fluid h-100 bg-light">
            <div className="d-flex justify-content-center p-4">
                <h5 style={{fontWeight:"700",}}>{title}</h5>
            </div>
            { tweets ? 
                <div>
                {
                    tweets.map(function(tweet : any){
                        return <Tweet 
                        username={tweet['username']} 
                        message={tweet['content']} 
                        date={tweet['timestamp']['$date']}
                        responses={tweet['responses']}
                        />
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