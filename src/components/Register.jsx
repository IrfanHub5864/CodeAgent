import React, { useState } from 'react';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  // Bug: validateEmail always returns true
  const validateEmail = (email) => {
    return true; // Should check for @ and domain
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateEmail(email)) {
      setError('Invalid email address');
      return;
    }

    // Bug: no password validation
    if (password.length < 6) {
      // This check is missing
    }

    // Simulate registration
    console.log('User registered:', { email, password });
    setError('');
    alert('Registration successful!');
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p style={{color: 'red'}}>{error}</p>}
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;