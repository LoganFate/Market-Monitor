import { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom';


const ProfilePage = () => {
//   const { userId } = useParams();
  const [profileData, setProfileData] = useState(null);
  const [plannerEntries, setPlannerEntries] = useState([]);

  useEffect(() => {
    // Replace with actual data fetching logic
    // For example, fetch from an API or use context/state management
    const fetchProfileData = async () => {
      try {
        const response = await fetch('/api/users/profile'); // Replace with your API endpoint
        const data = await response.json();
        setProfileData(data);
      } catch (error) {
        console.error('Failed to fetch profile data:', error);
      }
    };

    fetchProfileData();
  }, []);

  useEffect(() => {
    const fetchPlannerEntries = async () => {
      try {
        const response = await fetch('/api/planner');
        if (!response.ok) {
          throw new Error('Failed to fetch planner entries');
        }
        const data = await response.json();
        setPlannerEntries(data);
      } catch (error) {
        console.error('Failed to fetch planner entries:', error);
      }
    };


    fetchPlannerEntries();
  }, []);

  if (!profileData) {
    return <div>Loading profile...</div>;
  }

  return (
    <div>
    <div>
      <h1>User Profile</h1>
      <p>Name: {profileData.name}</p>
      <p> Username: {profileData.username}</p>
      <p>Email: {profileData.email}</p>
      <p>About: {profileData.user_about}</p>
      <p>Profile Pic: {profileData.profile_pic}</p>
      {/* Add more profile data as needed */}
    </div>
    {/* Planner Entries Section */}
<div>
  <h2>Planner Entries</h2>
  {plannerEntries.length > 0 ? (
    plannerEntries.map(entry => (
      <div key={entry.id}>
        <h3>{entry.category}</h3>
        <p>{entry.text}</p>
        {/* Format the date as needed */}
        <p>Created At: {entry.created_at}</p>
      </div>
    ))
  ) : (
    <p>No planner entries found.</p>
  )}
</div>
</div>
  );
};

export default ProfilePage;
