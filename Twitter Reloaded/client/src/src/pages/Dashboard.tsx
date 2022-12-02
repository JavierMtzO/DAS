import React, { useState } from "react";
import Container from 'react-bootstrap/Container';
import Tweets from "../components/FeedTweets";

export default function Dashboard() {

  const [data, setData] = React.useState<any[]>([])

  React.useEffect(() => {
    fetch("/tweets")
        .then((res) => res.json())
        .then((data) => setData(data));
  }, []);

  return (
    <Container fluid className='full-page-with-nav'>
      <div className='row mt-3 mt-md-5'>
        <h2>Dashboard</h2>
      </div>
      <hr />
      <Tweets />
      { data ? 
        <div>
          {
            data.map(function(tweet,index){
              return <p>{tweet['content']}</p>
            })
          }
        </div>
        :
        <div> </div>
      }
    </Container>
  );
}