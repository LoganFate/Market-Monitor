import { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom';
import './ProfilePage.css'


const ProfilePage = () => {
//   const { userId } = useParams();
  const [profileData, setProfileData] = useState(null);
  const [plannerEntries, setPlannerEntries] = useState([]);
  const [showAddPlanForm, setShowAddPlanForm] = useState(false);
  const [newPlan, setNewPlan] = useState({ planner_category: '', plan_text: '' });
  const [isEditMode, setIsEditMode] = useState(false);
  const [editingPlanId, setEditingPlanId] = useState(null);

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

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    const endpoint = isEditMode ? `/api/planner/${editingPlanId}` : '/api/planner';
    const method = isEditMode ? 'PUT' : 'POST';
    const body = JSON.stringify({
      planner_category: newPlan.planner_category,
      plan_text: newPlan.plan_text,
    });

    try {
      const response = await fetch(endpoint, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body,
      });
      if (!response.ok) {
        throw new Error('Failed to process plan');
      }
      const responseData = await response.json();

      if (isEditMode) {
        // Update the local state to reflect the edited plan
        setPlannerEntries(plannerEntries.map(entry => entry.id === editingPlanId ? responseData : entry));
      } else {
        // Add the new plan to the local state
        setPlannerEntries([...plannerEntries, responseData]);
      }
      resetFormAndExitEditMode(); // Reset form fields and exit edit mode
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleDeletePlan = async (planId) => {
    try {
      const response = await fetch(`/api/planner/${planId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete plan');
      }
      setPlannerEntries(plannerEntries.filter(entry => entry.id !== planId)); // Update UI
    } catch (error) {
      console.error('Failed to delete plan:', error);
    }
  };

  const handleEditPlan = (plan) => {
    setNewPlan({ planner_category: plan.category, plan_text: plan.text });
    setIsEditMode(true);
    setEditingPlanId(plan.id);
    setShowAddPlanForm(true); // Assuming you are using this state to toggle the visibility of the form
  };

  const resetFormAndExitEditMode = () => {
    setNewPlan({ planner_category: '', plan_text: '' });
    setIsEditMode(false);
    setEditingPlanId(null);
    setShowAddPlanForm(false);
  };

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
                    <button onClick={() => handleDeletePlan(entry.id)}>Delete</button>
                    <button onClick={() => handleEditPlan(entry)}>Edit</button>

                    <p><span className="detail-label">Created At:</span> {entry.created_at}</p>
                </div>
            ))
        ) : (
            <p>No planner entries found.</p>
        )}
    </section>
    {showAddPlanForm && (
  <form onSubmit={handleFormSubmit}>
    <input
      type="text"
      placeholder="Category"
      value={newPlan.planner_category}
      onChange={(e) => setNewPlan({ ...newPlan, planner_category: e.target.value })}
    />
    <textarea
      placeholder="Plan Text"
      value={newPlan.plan_text}
      onChange={(e) => setNewPlan({ ...newPlan, plan_text: e.target.value })}
    />
    <button type="submit">Add Plan</button>
    <button onClick={() => setShowAddPlanForm(false)}>Cancel</button>
  </form>
)}
<button onClick={() => setShowAddPlanForm(true)}>Add New Plan</button>
</div>
  );
};

export default ProfilePage;