import { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom';
import './ProfilePage.css'


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
    <div className="profile-page">
    <header className="profile-header">
        <h1>User Profile</h1>
    </header>
    <section className="profile-info">
        <div className="profile-details">
            <p><span className="detail-label">Name:</span> {profileData.name}</p>
            <p><span className="detail-label">Username:</span> {profileData.username}</p>
            <p><span className="detail-label">Email:</span> {profileData.email}</p>
            <p><span className="detail-label">About:</span> {profileData.user_about}</p>
            <p><span className="detail-label">Profile Pic:</span> <img src={profileData.profile_pic} alt="Profile" /></p>
        </div>
    </section>
    <section className="planner-entries">
        <h2>Planner Entries</h2>
        {plannerEntries.length > 0 ? (
            plannerEntries.map(entry => (
                <div key={entry.id} className="planner-entry">
                    <h3>{entry.category}</h3>
                    <p>{entry.text}</p>
                    <p><span className="detail-label">Created At:</span> {entry.created_at}</p>
                </div>
            ))
        ) : (
            <p>No planner entries found.</p>
        )}
    </section>
</div>
  );
};

export default ProfilePage;
