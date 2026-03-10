import React, { useState } from 'react';

const LoginButton = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Bug: handleSubmit is defined but not connected to form onSubmit
  const handleSubmit = (e) => {
    e.preventDefault();
    // Bug: calls onLogin but doesn't pass credentials
    onLogin();
  };

  return (
    <form>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginButton;