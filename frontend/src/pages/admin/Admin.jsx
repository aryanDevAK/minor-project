import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Changed useHistory to useNavigate
import axios from 'axios';
import NavBar from '../../components/NavBar.jsx/NavBar';
import Sidebar from '../../components/sidebar/Sidebar';
import AdminHome from '../adminHome/AdminHome';
import "./admin.css"

const AdminDashboard = () => {
  // const [username, setUsername] = useState('');
  // const [email, setEmail] = useState('');
  // const [profilePhoto, setProfilePhoto] = useState('');
  // const [notifications, setNotifications] = useState([]);
  // const navigate = useNavigate(); // Replaced useHistory with useNavigate

  // useEffect(() => {
  //   const token = localStorage.getItem('access_token');
  //   if (!token) {
  //     navigate('/login');
  //   } else {
  //     // Fetch profile data
  //     axios
  //       .get('/api/admin/profile', {
  //         headers: {
  //           Authorization: `Bearer ${token}`,
  //         },
  //       })
  //       .then((response) => {
  //         setUsername(response.data.username);
  //         setEmail(response.data.email);
  //         setProfilePhoto(response.data.profile_photo);
  //       })
  //       .catch((error) => {
  //         console.error(error);
  //       });
  
  //     // Fetch notifications
  //     axios
  //       .get('/api/admin/notifications', {
  //         headers: {
  //           Authorization: `Bearer ${token}`,
  //         },
  //       })
  //       .then((response) => {
  //         const notificationsData = Array.isArray(response.data) ? response.data : [];
  //         setNotifications(notificationsData);
  //       })
  //       .catch((error) => {
  //         console.error(error);
  //       });
  //   }
  // }, [navigate]);
  

  // const handleLogout = () => {
  //   localStorage.removeItem('access_token');
  //   navigate('/login'); // Replaced history.push with navigate
  // };

  // return (
  //   <div className="admin-dashboard">
  //     <div className="top-bar">
  //       <div className="profile">
  //         <img src={profilePhoto} alt="Profile" />
  //         <span>{username} ({email})</span>
  //         <button onClick={handleLogout}>Logout</button>
  //       </div>
  //       <div className="notifications">
  //         <button>Notifications ({notifications.length})</button>
  //         <ul>
  //           {notifications.map((notification, index) => (
  //             <li key={index}>{notification.message}</li>
  //           ))}
  //         </ul>
  //       </div>
  //     </div>
  //     <div className="left-nav">
  //       <ul>
  //         <li>
  //           <Link to="/admin/doctors">Doctors</Link>
  //         </li>
  //         <li>
  //           <Link to="/admin/departments">Departments</Link>
  //         </li>
  //         <li>
  //           <Link to="/admin/nurses">Nurses</Link>
  //         </li>
  //         <li>
  //           <Link to="/admin/staff">Staff</Link>
  //         </li>
  //         <li>
  //           <Link to="/admin/rooms">Rooms</Link>
  //         </li>
  //         <li>
  //           <Link to="/admin/labs">Labs</Link>
  //         </li>
  //         <li>
  //           <Link to="/admin/patients">Patients</Link>
  //         </li>
  //       </ul>
  //     </div>
  //     <div className="main-content">
  //       {/* Render main content here */}
  //     </div>
  //   </div>
  // );

  const [sidebar, setSidebar] = useState(true)
  const [activeComponent, setActiveComponent] = useState("Dashboard")

  return (
    <div className="admin-dashboard">
      <NavBar setsidebar={setSidebar}/>
      <Sidebar sidebar={sidebar} setActiveComponent={setActiveComponent} activeComponent={activeComponent} />
      <div className="container">
        <AdminHome activeComponent={activeComponent} />
      </div>
    </div>
  )
};

export default AdminDashboard;