import React from 'react';
import dashboard from "../../../assets/dashboard.png";
import settings from "../../../assets/settings.png";
import logout from "../../../assets/logout.png";
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ sidebar, setActiveComponent, activeComponent }) => {
  const navigate = useNavigate();

    const handleLogout = () => {
      localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('mobile_num');
    navigate("/login");
  };

    return (
        <div className={`sidebar ${sidebar?"":"small-sidebar"}`}>
          <div className="profile">
              <h2>Welcome,</h2>
              <h3></h3>
          </div>
          <hr />
          <div className="shortcut-link">
              <div className={`side-link ${activeComponent === "Dashboard" ? "active" : ""}`} onClick={() => setActiveComponent('Dashboard')}>
                  <img src={dashboard} alt="dashboard icon" /><p>Dashboard</p>
              </div>
              <div className={`side-link ${activeComponent === "MedixifyAI" ? "active" : ""}`} onClick={() => setActiveComponent('MedixifyAI')}>
                  <img src={dashboard} alt="dashboard icon" /><p>Medixify AI</p>
              </div>
          </div>
          <hr />
          <div className="personal-settings">
              <h3>Personal Settings</h3>
              <div className={`side-link ${activeComponent === "Settings" ? "active" : ""}`} onClick={() => setActiveComponent('Settings')}>
                  <img src={settings} alt="settings icon" /><p>Settings</p>
              </div>
              <div className="side-link" onClick={handleLogout}>
                  <img src={logout} alt="logout icon" /><p>Logout</p>
              </div>
          </div>
      </div>
  );
}

export default Sidebar;
