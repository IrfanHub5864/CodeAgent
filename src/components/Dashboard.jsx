import DOMPurify from 'dompurify';

const fetchDashboardData = async () => {
  try {
    const response = await fetch('/api/dashboard-data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    return null;
  }
};

const renderStats = (data) => {
  if (!data) return null; // Add null check

  const sanitizedDescription = DOMPurify.sanitize(data.description);
  return (
    <div>
      <p dangerouslySetInnerHTML={{ __html: sanitizedDescription }} />
      {/* Other stats rendering logic */}
    </div>
  );
};