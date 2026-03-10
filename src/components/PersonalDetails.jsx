// src/components/PersonalDetails.jsx
import React, { useState } from 'react';

const PersonalDetails = () => {
  const [email, setEmail] = useState('');
  const [userData, setUserData] = useState({}); // Define userData

  const handleSubmit = (event) => {
    event.preventDefault();
    // Remove or fix console.log statement
    // console.log(userData); // If userData is not used, remove this line
    console.log('Form submitted successfully');
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Email:</label>
        <input type="email" value={email} onChange={(event) => setEmail(event.target.value); } />
      </div> {/* Add closing tag */}
      <button type="submit">Submit</button>
    </form>
  );
};

export default PersonalDetails;