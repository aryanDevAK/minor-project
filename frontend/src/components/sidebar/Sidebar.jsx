import React from 'react'
import "./sidebar.css"
import profile_pic from "../../assets/account.png"
import dashboard from "../../assets/dashboard.png"

const Sidebar = () => {
  return (
      <div className="sidebar">
          <div className="profile">
              <h3>Welcome John Doe</h3>
              <img src={profile_pic} alt="profile-picture" />
          </div>
          <hr />
          <div className="shortcut-link">
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Dashboard</p>
              </div>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Patient</p>
              </div>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Doctors</p>
              </div>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Nurses</p>
              </div>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Staff</p>
              </div>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Labs</p>
              </div>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Appointments</p>
              </div>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Pharmacies</p>
              </div>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Reports</p>
              </div>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Inventory</p>
              </div>
          </div>
          <hr />
          <div className="personal-settings">
              <h3>Personal Settings</h3>
              <div className="side-link">
                  <img src={dashboard} alt="" /><p>Settings</p>
              </div>
              <button className='btn'>Logout</button>
          </div>
    </div>
  )
}

export default Sidebar