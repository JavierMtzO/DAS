import React, { useState } from "react";
import Container from 'react-bootstrap/Container';
import Tweets from "../components/FeedTweets";

export default function Dashboard() {

  const [data, setData] = React.useState<any[]>([])

  React.useEffect(() => {
    fetch("/newtweets")
        .then((res) => res.json())
        .then((data) => setData(data));
  }, []);

  if(data) {
    console.log(data);
  }

  return (
    <Container fluid className='full-page-with-nav'>
      <div className='row mt-3 mt-md-5'>
        <h2>Dashboard</h2>
      </div>
      <hr />
      {
        data ?
        <Tweets title="Latest tweets" tweets={data}/>
        :
        <div></div>
      }
    </Container>
  );
}