// src/components/LoginButton.jsx
import React from 'react';
import { handleSubmit } from '../auth';

const LoginButton = () => {
  const handleLoginClick = (event) => {
    event.preventDefault(); // Prevent default form submission behavior if needed
    handleSubmit(); // Call the actual submission handler
  };

  return (
    <button type="submit" onClick={handleLoginClick}>Login</button>
  );
};

export default LoginButton;