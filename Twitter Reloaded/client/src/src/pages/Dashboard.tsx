import React, { useState } from "react";
import Container from 'react-bootstrap/Container';
import Tweets from "../components/FeedTweets";
import Input from "../components/Input";
import Button from "../components/Button";

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
      <div className="row mt-3 mt-md-5">
        <div className="col-7">
          <Input type="text" divClass="form-floating col-lg-7 mb-4" inputClass="form-control"
                inputId="tweetBox" placeholder="Escribe tu tweet (300 char)" labelClass="form-label ps-4" maxLength={40}
                feedbackClass="px-3 pt-2 text-light" feedbackText={""}
                />
          <div className="col-3">
            <Button 
                    className="btn-primary fw-bold "
                    btnType="submit"
                    btnText="Post"
                    padding="py-3"/>     

          </div>
        </div>
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