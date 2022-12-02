import React from "react";

export default function Tweets()  {
    return (
        <div className="container-fluid h-100 bg-light">
            <div className="d-flex justify-content-center p-4">
                <h3 style={{fontWeight:"700",}}>Latest tweets from HeyBerns</h3>
            </div>

            <div className="m-2 bg-info">
                <div className="d-flex justify-content-between">
                    <h5 style={{fontWeight:"400",}}>@HeyBerns</h5>
                    <p style={{fontWeight:"100",}}>02/12/2022</p>
                </div>
                <div className="d-flex justify-content-center">
                    <h6 style={{fontWeight:"600",}}>Hoy me siento tremendamente impotente</h6>
                </div>
            </div>

            <div className="m-2 bg-info">
                <div className="d-flex justify-content-between">
                    <h5 style={{fontWeight:"400",}}>@HeyBerns</h5>
                    <p style={{fontWeight:"100",}}>02/12/2022</p>
                </div>
                <div className="d-flex justify-content-center">
                    <h6 style={{fontWeight:"600",}}>Hoy me siento tremendamente impotente</h6>
                </div>
            </div>

            <div className="m-2 bg-info">
                <div className="d-flex justify-content-between">
                    <h5 style={{fontWeight:"400",}}>@HeyBerns</h5>
                    <p style={{fontWeight:"100",}}>02/12/2022</p>
                </div>
                <div className="d-flex justify-content-center">
                    <h6 style={{fontWeight:"600",}}>Hoy me siento tremendamente impotente</h6>
                </div>
            </div>


        </div>
    );
}