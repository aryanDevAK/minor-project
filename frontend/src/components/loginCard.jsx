import React from 'react';
import "../styles/loginCard.css"

const LoginCard = ({ name, data, onClick }) => {
  const handleLogin = () => {
    onClick(name);
  };

  return (
    <div>
      <div className='login-card'>
        <h2>{name.charAt(0).toUpperCase() + name.slice(1)} Login</h2>
        <p>{data}</p>
        <button onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
};

export default LoginCard;