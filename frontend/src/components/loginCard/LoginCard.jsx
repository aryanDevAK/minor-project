import React from 'react';
import "./loginCard.css"

const LoginCard = ({ name, data, onClick, image }) => {
  const handleLogin = () => {
    onClick(name);
  };

  return (
    <div className='login-card'>
      <img src={image} alt="logo" />
      <div>
        <h2>{name.charAt(0).toUpperCase() + name.slice(1)} Login</h2>
        <p>{data}</p>
      </div>
      <button className='btn' onClick={handleLogin}>Login</button>
    </div>
  );
};

export default LoginCard;