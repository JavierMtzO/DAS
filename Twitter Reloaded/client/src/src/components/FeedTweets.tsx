import React from "react";
import Tweet from "./Tweet/Tweet";

type Props = {
    username: string,
    message: string,
    date: string
  }

export default function Tweets()  {
    return (
        <div className="container-fluid h-100 bg-light">
            <div className="d-flex justify-content-center p-4">
                <h3 style={{fontWeight:"700",}}>Latest tweets from HeyBerns</h3>
            </div>
            <Tweet username="@HeyBerns" message="Elon Musk mlp" date="04/12/2022"/>
            <Tweet username="@HeyBerns" message="Elon Musk mlp" date="05/12/2022"/>     
            {/* <Post/> */}
        </div>
    );
}