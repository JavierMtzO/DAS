import React from "react";
import BtnBrand from "./BtnBrand";
import NavCollapse from "./NavCollapse";
import SearchBar from "./SearchBar";
import Button from "../Button";
// import NavList from "./NavList";
import { useNavigate } from "react-router-dom";
import { deleteToken, getToken } from "../../services/tokenUtilities";

export default function Navbar() {
  const navigate = useNavigate()
  // const token = getToken()

  return (
    <nav className="navbar fixed-top navbar-expand-md navbar-light bg-light border-bottom border-3">
      <div className="container-fluid">
        <BtnBrand className="navbar-brand fw-bold fs-1 lh-base" />
        <NavCollapse id="navbarContent">
          <SearchBar
            formClass="ms-auto me-md-2 my-2 my-lg-0"
            borderClass="border-primary"
            searchPlaceholder="Buscar" />
          <div className="navbar-nav">
            <Button
              onClick={() => navigate('/login')}
              className="btn-dark rounded-pill fw-bold"
              padding="px-lg-5 px-3"
              btnType="button"
              btnText="Iniciar sesión" />
            <Button
              onClick={() => navigate('/user_profile')}
              className="btn-primary rounded-pill fw-bold"
              padding="px-lg-5 px-3"
              btnType="button"
              btnText="Mi perfil" />
          </div>
          {/* TODO: Show until we have a view for the user's profile */}
          {/* {token && <NavList />} */}
        </NavCollapse>
      </div>
    </nav>
  )
}