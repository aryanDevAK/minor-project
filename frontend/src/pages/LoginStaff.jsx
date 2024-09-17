import React, { useState } from 'react';
import axios from 'axios';
import "../styles/loginPages.css"

const LoginPageStaff = () => {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const data = {
        id: userId,
        password: password
      }
      const url = 'http://localhost:5000/login'
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
        alert(`Login successful! ${responseData.message}`);
      } else {
        const responseData = await response.json();
        setError(`Login failed: ${responseData.message}`);
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
          placeholder="User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <input
          type="password"
          className="login-input"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="login-button">Login</button>
        {error && <div className="error-message">{error}</div>}
      </form>
    </div>
  );
};

export default LoginPageStaff;