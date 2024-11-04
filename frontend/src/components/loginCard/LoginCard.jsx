import React from 'react';
import "./loginCard.css"

const LoginCard = ({ name, data, onClick, image, buttonname, myClass, btnClass }) => {
  const handleLogin = () => {
    onClick(name);
  };

  return (
    <div className={`login-card ${myClass}`}>
      <img src={image} alt="logo" />
      <div>
        <h2>{name.charAt(0).toUpperCase() + name.slice(1)}</h2>
        <p>{data}</p>
      </div>
      <button className={btnClass} onClick={handleLogin}>{buttonname}</button>
    </div>
  );
};

export default LoginCard;