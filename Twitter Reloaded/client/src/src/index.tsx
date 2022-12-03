import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle';
import './custom.scss';
import Navbar from './components/Navbar';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import HomeLogin from './pages/HomeLogin';
import HomeRegister from './pages/HomeRegister';
import UserProfile from './pages/UserProfile';
import Dashboard from './pages/Dashboard'
import GuestRoute from './utils/GuestRoute';
import ProtectedRoute from './utils/ProtectedRoute';

ReactDOM.render(
  <BrowserRouter>
    <Navbar />
    <Routes>
      <Route path='/' element={<Dashboard />} />
      {/* <Route element={<ProtectedRoute/>}> */}
        <Route path='/user_profile' element={<UserProfile />} />
      {/* </Route> */}
      {/* <Route element={<GuestRoute />}> */}
        <Route path='/login' element={<HomeLogin />} />
        <Route path='/register' element={<HomeRegister />} />
      {/* </Route> */}
    </Routes>
  </BrowserRouter>,
  document.getElementById('root')
);
