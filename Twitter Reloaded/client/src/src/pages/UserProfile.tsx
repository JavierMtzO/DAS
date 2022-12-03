import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Flush from "../components/Flush";
import Button from "../components/Button";
import { deleteToken } from "../services/tokenUtilities";
import Tweets from "../components/FeedTweets";
import { useNavigate } from "react-router-dom";

export default function UserProfile() {
  const [user, setUser] = useState<User>();
  // const username : string = sessionStorage.getItem('userName')!;
  const username : string = "HeyBerns"
  const navigate = useNavigate();

  return (
    <div className="full-page-with-nav container-fluid">
      <div className="row h-100">
        <div className="d-none d-md-block col-12 col-lg-3">
          <Sidebar
            title="Mi Perfil"
            name={username}
            edit="Editar foto">
              <Flush
                id="One"
                title="Mi información"
                userData={user ?? user} />
              <div className="row my-5 px-3">
                <Button 
                    onClick={() => {
                      deleteToken();
                      navigate('/login');
                    }}
                    className="btn-outline-dark btn-sm rounded-pill fw-bold ms-lg-2"
                    padding={''}
                    btnType="button"
                    btnText="Cerrar sesión"/>
              </div>
          </Sidebar>
        </div>
        <div className="col-12 col-lg-9 py-3 py-lg-5">  
          {/* <Tweets />         */}
        </div>
      </div>
    </div>
  )
}