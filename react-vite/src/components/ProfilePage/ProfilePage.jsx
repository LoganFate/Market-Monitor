import { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom';
import './ProfilePage.css'
import { useModal } from '../../context/Modal';


const ProfilePage = () => {
//   const { userId } = useParams();
  const [profileData, setProfileData] = useState(null);
  const [plannerEntries, setPlannerEntries] = useState([]);
  const [showAddPlanForm, setShowAddPlanForm] = useState(false);
  const [newPlan, setNewPlan] = useState({ planner_category: '', plan_text: '' });
  const [isEditMode, setIsEditMode] = useState(false);
  const [editingPlanId, setEditingPlanId] = useState(null);
  const { setModalContent, closeModal } = useModal();
  const [formErrors, setFormErrors] = useState({});


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

    setFormErrors({});

    let errors = {};
    if (newPlan.planner_category.length > 50) {
      errors.planner_category = "Category name is too long (max 50 characters).";
    }
    if (newPlan.plan_text.length > 500) {
      errors.plan_text = "Plan description is too long (max 500 characters).";
    }

    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

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

  const requestDeleteConfirmation = (planId) => {
    setModalContent(
      <div className="delete-confirmation-modal">
        <div className="modal-content">
          <p>Are you sure you want to delete this plan?</p>
          <div className="modal-actions">
            <button className="modal-button confirm" onClick={() => handleDeletePlan(planId)}>Confirm</button>
            <button className="modal-button cancel" onClick={closeModal}>Cancel</button>
          </div>
        </div>
      </div>
    );
  };
  const handleDeletePlan = async (planId) => {
    closeModal();
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
    setShowAddPlanForm(true);
    toggleAddButtonVisibility();
  };

  const resetFormAndExitEditMode = () => {
    setNewPlan({ planner_category: '', plan_text: '' }); // Clear form fields
    setIsEditMode(false); // Reset edit mode
    setEditingPlanId(null); // Clear editing ID
    setShowAddPlanForm(false); // Hide form
    setFormErrors({}); // Clear any form errors
    toggleAddButtonVisibility();
  };

  function formatDate(dateString) {
    const date = new Date(dateString);
    const month = date.getMonth() + 1; // getMonth() returns 0-11
    const day = date.getDate();
    const year = date.getFullYear();
    return `${month}-${day}-${year}`;
  }

  const toggleAddButtonVisibility = () => {
    const addButton = document.querySelector('.add-plan-button');
    if (addButton) {
      addButton.classList.toggle('hidden');
    }
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
        </div>
    </section>
    <section className="planner-entries">
        <h2>Planner Entries</h2>
        {plannerEntries.length > 0 ? (
            plannerEntries.map(entry => (
                <div key={entry.id} className="planner-entry">
                    <h3 className='category'>{entry.category}</h3>
                    <p>{entry.text}</p>
                    <button className="button" onClick={() => requestDeleteConfirmation(entry.id)}>Delete</button>
                    <button className="button" onClick={() => handleEditPlan(entry)}>Edit</button>
                    <p>{formatDate(entry.created_at)}</p>
                </div>
            ))
        ) : (
            <p>No planner entries found.</p>
        )}
    </section>
  <div className="form-container">
    { showAddPlanForm && (
  <form onSubmit={handleFormSubmit}>
    <div className="input-group">
      <input
        type="text"
        placeholder="Category"
        className="input-field"
        value={newPlan.planner_category}
        onChange={(e) => setNewPlan({ ...newPlan, planner_category: e.target.value })}
      />
      {formErrors.planner_category && <p className="form-error">{formErrors.planner_category}</p>}
    </div>

    <div className="input-group">
      <textarea
        placeholder="Plan Text"
        className="textarea-field"
        value={newPlan.plan_text}
        onChange={(e) => setNewPlan({ ...newPlan, plan_text: e.target.value })}
      />
      {formErrors.plan_text && <p className="form-error">{formErrors.plan_text}</p>}
    </div>

    <div className="button-group">
      <button className="button submit-button" type="submit">{isEditMode ? 'Update Plan' : 'Add Plan'}</button>
      <button className="button cancel-button" onClick={resetFormAndExitEditMode}>Cancel</button>
    </div>
  </form>
    )}
  <button className="button add-plan-button" onClick={() => { setShowAddPlanForm(true); toggleAddButtonVisibility(); }}>Add New Plan</button>
</div>

</div>
  );
};

export default ProfilePage;
