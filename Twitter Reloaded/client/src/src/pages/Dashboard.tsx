import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Tweets from "../components/FeedTweets";
import Input from "../components/Input";
import Button from "../components/Button";
import Form from "../components/Form";
import { postTweet } from "../services/userCalls";

export default function Dashboard() {

  const [data, setData] = React.useState<any[]>([])
  
  const navigate = useNavigate()
  const location = useLocation()

  const [usernameFeedback, setUsernameFeedback] = useState("")
  const [passwordFeedback, setPasswordFeedback] = useState("")

//   React.useEffect(() => {
//     const fetchUserData = async () => {
//         try {
//             const loggedInUser : User = await getLoggedInUser();
//             setName(loggedInUser.name);
//             setUsername(loggedInUser.username);
//             setEmail(loggedInUser.email);
//             setPhoneNumber(loggedInUser.phoneNumber);
//         } catch (error) {
//             console.log(error);
//         }
//     }
//     fetchUserData();
// }, []);


  React.useEffect(() => {
    fetch("/newtweets")
        .then((res) => res.json())
        .then((data) => setData(data));
  }, []);

  if(data) {
    console.log(data);
  }

  const onSubmit: (e: React.FormEvent) => void = async (e) => {
    e.preventDefault();
    const target = e.target as typeof e.target & {
      content : {value: string}
    };

    try {
      await postTweet(target.content.value);

      const loc = location as typeof location & {
        state: {from: string}
      }

      if (loc.state && loc.state.from) {
        navigate(loc.state.from);
        return;
      }

      navigate("/register")

    } catch (error) {
      const err = error as typeof error & ErrorResponse;
      console.log(err.msg)
    }
  }

  return (
    <Container fluid className='full-page-with-nav'>
      <div className='row mt-3 mt-md-5'>
        <h2>Dashboard</h2>
      </div>
      <hr />
      <div className="row mt-3 mt-md-5">
        <div className="col-7">
          <Form className="row mt-5 pt-4" onSubmit={onSubmit} noValidate={true}>
            <Input type="text" divClass="form-floating col-lg-7 mb-4" inputClass="form-control"
                  inputId="content" placeholder="Escribe tu tweet (300 char)" labelClass="form-label ps-4" maxLength={40}
                  feedbackClass="px-3 pt-2 text-light" feedbackText={""}
                  />
            <div className="col-3">
              <Button 
                      className="btn-primary fw-bold "
                      btnType="submit"
                      btnText="Post"
                      padding="py-3"/>
            </div>
          </Form>
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