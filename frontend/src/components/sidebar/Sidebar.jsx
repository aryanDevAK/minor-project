import React from 'react'
import "./sidebar.css"
import profile_pic from "../../assets/account.png"
import dashboard from "../../assets/dashboard.png"
import nurse from "../../assets/nurse.png"
import patient from "../../assets/person1.png"
import prescription from "../../assets/prescription.png"
import settings from "../../assets/settings.png"
import doctor from "../../assets/sthetescope.png"
import admin from "../../assets/admin.png"
import inventory from "../../assets/inventory.png"
import reports from "../../assets/reports.png"
import labs from "../../assets/labs.png"
import pharmacy from "../../assets/pharmacy.png"
import logout from "../../assets/logout.png"

const Sidebar = ({sidebar, setActiveComponent, activeComponent}) => {
  return (
      <div className={`sidebar ${sidebar?"":"small-sidebar"}`}>
          <div className="profile">
          <img src={profile_pic} alt="profile-picture" className='profile-img' />
              <h3>Welcome John Doe</h3>
          </div>
          <hr />
          <div className="shortcut-link">
              <div className={`side-link ${activeComponent==="Dashboard"?"active":""}`} onClick={() => setActiveComponent('Dashboard')}>
                  <img src={dashboard} alt="" /><p>Dashboard</p>
              </div>
              <div className={`side-link ${activeComponent==="Patient"?"active":""}`} onClick={() => setActiveComponent('Patient')}>
                  <img src={patient} alt="" /><p>Patient</p>
              </div>
              <div className={`side-link ${activeComponent==="Doctor"?"active":""}`} onClick={() => setActiveComponent('Doctor')}>
                  <img src={doctor} alt="" /><p>Doctors</p>
              </div>
              <div className={`side-link ${activeComponent==="Nurse"?"active":""}`} onClick={() => setActiveComponent('Nurse')}>
                  <img src={nurse} alt="" /><p>Nurses</p>
              </div>
              <div className={`side-link ${activeComponent==="Staff"?"active":""}`} onClick={() => setActiveComponent('Staff')}>
                  <img src={admin} alt="" /><p>Staff</p>
              </div>
              <div className={`side-link ${activeComponent==="Labs"?"active":""}`} onClick={() => setActiveComponent('Labs')}>
                  <img src={labs} alt="" /><p>Labs</p>
              </div>
              <div className={`side-link ${activeComponent==="Appointments"?"active":""}`} onClick={() => setActiveComponent('Appointments')}>
                  <img src={prescription} alt="" /><p>Appointments</p>
              </div>
              <div className={`side-link ${activeComponent==="Pharmacies"?"active":""}`} onClick={() => setActiveComponent('Pharmacies')}>
                  <img src={pharmacy} alt="" /><p>Pharmacies</p>
              </div>
              <div className={`side-link ${activeComponent==="Reports"?"active":""}`} onClick={() => setActiveComponent('Reports')}>
                  <img src={reports} alt="" /><p>Reports</p>
              </div>
              <div className={`side-link ${activeComponent==="Inventory"?"active":""}`} onClick={() => setActiveComponent('Inventory')}>
                  <img src={inventory} alt="" /><p>Inventory</p>
              </div>
          </div>
          <hr />
          <div className="personal-settings">
              <h3>Personal Settings</h3>
              <div className={`side-link ${activeComponent==="Settings"?"active":""}`} onClick={() => setActiveComponent('Settings')}>
                  <img src={settings} alt="" /><p>Settings</p>
              </div>
              <div className="side-link">
                  <img src={logout} alt="" /><p>Logout</p>
              </div>
          </div>
    </div>
  )
}

export default Sidebar