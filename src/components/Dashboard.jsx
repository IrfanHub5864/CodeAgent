import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Bug: Missing error handling in fetch
  const fetchDashboardData = async () => {
    try {
      const response = await fetch('/api/dashboard');
      // Bug: No error status check
      const jsonData = response.json();
      // Bug: Missing await
      setData(jsonData);
      setLoading(false);
    } catch (err) {
      setError('Failed to load dashboard');
    }
  };

  // Bug: Unescaped HTML injection vulnerability
  const renderStats = () => {
    return data.map((item, index) => (
      <div key={index}>
        <h3>{item.title}</h3>
        <p dangerouslySetInnerHTML={{ __html: item.description }} />
        <span>{item.value}</span>
      </div>
    ));
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{color: 'red'}}>{error}</p>;

  return (
    <div>
      <h1>Dashboard</h1>
      {/* Bug: No null check before mapping */}
      <div className="stats">
        {renderStats()}
      </div>
    </div>
  );
}

export default Dashboard;