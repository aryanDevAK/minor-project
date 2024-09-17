import React, { useState } from 'react';
import axios from 'axios';
import "../styles/loginPages.css"

const LoginPagePatient = () => {
  const [mobileNum, setMobileNum] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const data = {
        mobile_num: mobileNum
      }
      const url = 'http://localhost:5000/login/patient'
      const options = {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json'
        }
      }
      const response = await fetch(url, options);

      if (response.ok) {
        const responseData = await response.json();
        localStorage.setItem('access_token', responseData.access_token);
        localStorage.setItem('refresh_token', responseData.refresh_token);
        alert(responseData.message);
      } else {
        const responseData = await response.json();
        alert(responseData.message)
      }
    } catch (error) {
      setError(`Login failed: ${error.message}`);
    }
  };

  return (
    <div className='login-container'>
      <form onSubmit={handleLogin} className="login-form">
        <input
          type="text"
          className="login-input"
          placeholder="Mobile Number"
          value={mobileNum}
          onChange={(e) => setMobileNum(e.target.value)}
        />
        <button type="submit" className="login-button">Login</button>
        {error && <div className="error-message">{error}</div>}
      </form>
    </div>
  );
};

export default LoginPagePatient;