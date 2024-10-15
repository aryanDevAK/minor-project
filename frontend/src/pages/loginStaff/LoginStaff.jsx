import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import ClipLoader from "react-spinners/ClipLoader"; // Import ClipLoader from react-spinners
import "../loginPatient/login.css";
import Notification from '../../components/notification/Notification';

const LoginPageStaff = () => {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [notificationMessage, setNotificationMessage] = useState(""); // For notification message
  const [loading, setLoading] = useState(false); // New state for loader
  const navigate = useNavigate(); // Replaced useHistory with useNavigate
  
  const fetchUserData = async (userId) => {
    const token = localStorage.getItem('access_token');
    if (!token || !userId) return;
  
    try {
      const response = await axios.get(`https://minor-project-dxsv.onrender.com/get/staff/${userId}`, {
        headers: {
          Authorization: `Bearer ${token}` 
        }
      });
  
      if (response.data) {
        const { name, email, role } = response.data; 
        localStorage.setItem('user_name', name);
        localStorage.setItem('user_email', email);
        localStorage.setItem('user_role', role);
      }
    } catch (error) {
      console.error('Failed to fetch user data:', error);
      setError('Failed to retrieve user information');
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true); 
    setError(null);
    try {
      const data = {
        id: userId,
        password: password
      };
      const url = 'https://minor-project-dxsv.onrender.com/login'
      const options = {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json'
        }
      };
      const response = await fetch(url, options);

      if (response.ok) {
        const responseData = await response.json();
        localStorage.setItem('access_token', responseData.access_token);
        localStorage.setItem('refresh_token', responseData.refresh_token);
        localStorage.setItem('user_id', userId);

        await fetchUserData(userId); 
        
        setNotificationMessage(`Login successful! ${responseData.message}`);
        setTimeout(() => setNotificationMessage(""), 2000);

        const role = responseData.role;
        if (role === 'admin') {
          navigate('/admin');
        } else if (role === 'doctor') {
          navigate('/doctor-dashboard');
        } else if (role === 'nurse') {
          navigate('/nurse-dashboard');
        } else if (role === 'staff') {
          navigate('/staff-dashboard');
        } else {
          setError('Unknown role: Unable to redirect.');
        }
      } else {
        const responseData = await response.json();
        setError(`${responseData.message}`);
        setNotificationMessage(`${responseData.message}`); // Set notification for error
        setTimeout(() => setNotificationMessage(""), 2000);
      }
    } catch (error) {
      setError(`${error.message}`);
      setNotificationMessage(`${error.message}`); // Set notification for error
      setTimeout(() => setNotificationMessage(""), 2000);
    } finally {
      setLoading(false); // Set loading to false when request finishes
    }
  };

  return (
    <div className='login-container'>
      <form onSubmit={handleLogin} className="login-form">
        <input
          type="text"
          className="login-input"
          placeholder="User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          disabled={loading} // Disable inputs when loading
        />
        <input
          type="password"
          className="login-input"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading} // Disable inputs when loading
        />
        <button type="submit" className="btn login-btn" disabled={loading}>Login</button>
        <p>Forgot Password?</p>
      </form>

      {/* Show the loader while loading is true */}
      {loading && (
        <div className="loader">
          <ClipLoader color="#093594" size={50} />
        </div>
      )}
      
      {notificationMessage && <Notification message={notificationMessage} type={error ? 'error' : 'success'} />}
    </div>
  );
};

export default LoginPageStaff;
