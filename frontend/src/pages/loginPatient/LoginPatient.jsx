import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import ClipLoader from "react-spinners/ClipLoader"; 
import "../loginPatient/login.css";
import Notification from '../../components/notification/Notification';

const LoginPagePatient = () => {
  const [mobileNum, setMobileNum] = useState("");
  const [error, setError] = useState(null);
  const [notificationMessage, setNotificationMessage] = useState(""); 
  const [loading, setLoading] = useState(false); 
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true); 
    setError(null);
    try {
      const data = { mobile_num: mobileNum };
      const url = 'https://minor-project-dxsv.onrender.com/login/patient';
      const response = await axios.post(url, data, {
        headers: { 'Content-Type': 'application/json' }
      });

      if (response.data) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('mobile_num', mobileNum);
        setNotificationMessage(`Login successful! ${response.data.message}`);
        setTimeout(() => setNotificationMessage(""), 2000);
        
        // Redirect to the patient's dashboard
        navigate('/patient-dashboard');
      }
    } catch (error) {
      const errorMessage = error.response ? error.response.data.message : error.message;
      setError(errorMessage);
      setNotificationMessage(errorMessage);
      setTimeout(() => setNotificationMessage(""), 2000);
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div className='login-outer'>
      <div className="login-bg">
        <h2>Welcome Back</h2>
        <h3>Welcome to Medixify! Please log in with your registered mobile number to access your personalized dashboard. Here, you can easily view and manage your health information, appointments, and more.<br/> For any health-related questions or assistance, don’t hesitate to use the Medixify AI Assistant, our smart tool designed to support you. The assistant provides insights into common health concerns, offers wellness advice, and suggests diet plans based on your medical records.<br/> Our goal is to make your healthcare experience smoother and more informed. Thank you for choosing Medixify for your healthcare needs!</h3>
      </div>
      <div className='login-container'>
        <h2>Login</h2>
        <form onSubmit={handleLogin} className="login-form">
          <label htmlFor="mobile-num">Mobile Number</label>
          <input type="text" className="login-input" name='mobile-num' value={mobileNum} onChange={(e) => setMobileNum(e.target.value)} disabled={loading} />
          <button type="submit" className="btn login-btn" disabled={loading}>Login</button>
        </form>

      {loading && (
        <div className="loader">
          <ClipLoader color="#093594" size={50} />
        </div>
      )}

      {notificationMessage && <Notification message={notificationMessage} type={error ? 'error' : 'success'} />}
      </div>
      </div>
  );
};

export default LoginPagePatient;
