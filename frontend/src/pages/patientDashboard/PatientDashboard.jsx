import React, { useState } from 'react';
import NavBar from '../../components/PatientComponents/Navbar/NavBar';
import Sidebar from '../../components/PatientComponents/Sidebar/Sidebar';
import PatientHome from './patientHome/PatientHome';

const PatientDashboard = () => {
  const [sidebar, setSidebar] = useState(true);
  const [activeComponent, setActiveComponent] = useState("Dashboard"); // Manage active link state

  return (
    <div className="admin-dashboard">
      <NavBar setSidebar={setSidebar} />
      <Sidebar sidebar={sidebar} setActiveComponent={setActiveComponent} activeComponent={activeComponent} />
      <div className={`container ${sidebar?"":"large-container"}`}>
        <PatientHome activeComponent={activeComponent} />
      </div>
    </div>
  );
}

export default PatientDashboard;
