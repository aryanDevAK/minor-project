import React from 'react';
import { Link } from 'react-router-dom';
import menu from "../../../assets/menu.png";
import logo from "../../../assets/logo-color.png";
import notification from "../../../assets/notification.png";

const NavBar = ({ setSidebar }) => {
  return (
    <nav className='flex-div'>
      <div className="nav-left flex-div">
        <img 
          src={menu} 
          alt="menu icon" 
          onClick={() => setSidebar(prev => !prev)} // Toggle sidebar
        />
        <Link to="/patient-dashboard">
          <img className='logo' src={logo} alt="logo" />
        </Link>
      </div>  
      <div className="nav-right flex-div">
        <img src={notification} alt="notification icon" />
      </div>
    </nav>
  );
}

export default NavBar;
