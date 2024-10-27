import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; 
import NavBar from '../../components/NavBar.jsx/NavBar';
import Sidebar from '../../components/sidebar/Sidebar';
import AdminHome from '../adminHome/AdminHome';
import "./admin.css"

const AdminDashboard = () => {
  const [sidebar, setSidebar] = useState(true);
  const [activeComponent, setActiveComponent] = useState("Dashboard");
  const [userData, setUserData] = useState({});

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    const username = localStorage.getItem('user_name');
    const email = localStorage.getItem('user_email');
    const role = localStorage.getItem('user_role');

    if (username) {
      setUserData({ username, email, role, userId });
    } else {
      setUserData("NULL")
    }
  }, []);

  return (
    <div className="admin-dashboard">
      <NavBar setsidebar={setSidebar} userid={userData.userId} />
      <Sidebar 
        sidebar={sidebar} 
        setActiveComponent={setActiveComponent} 
        activeComponent={activeComponent} 
        userData={userData} // Pass user data to sidebar
      />
      <div className={`container ${sidebar?"":"large-container"}`}>
        <AdminHome activeComponent={activeComponent} />
      </div>
    </div>
  );
};

export default AdminDashboard;
