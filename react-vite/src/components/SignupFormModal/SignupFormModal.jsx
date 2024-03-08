import { useState } from "react";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import { thunkSignup } from "../../redux/session";
import "./SignupForm.css";

function SignupFormModal() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [aboutMe, setAboutMe] = useState("");
  const [profilePic, setProfilePic] = useState("");
  const [errors, setErrors] = useState({});
  const { closeModal } = useModal();

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const validateForm = () => {
    const newErrors = {};
    if (!emailRegex.test(email)) {
      newErrors.email = "Invalid email format.";
    }
    if (password.length < 8) {
      newErrors.password = "Password must be at least 8 characters long.";
    }
    if (password !== confirmPassword) {
      newErrors.confirmPassword = "Confirm Password field must match the Password field.";
    }
    if (username.length < 3 || username.length > 20) {
      newErrors.username = "Username must be between 3 and 20 characters long.";
    }
    if (aboutMe.length < 10 || aboutMe.length > 300) {
      newErrors.user_about = "About Me must be between 10 and 300 characters long.";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    const serverResponse = await dispatch(
      thunkSignup({
        email,
        username,
        password,
        user_about: aboutMe,
      })
    );

    if (serverResponse) {
      setErrors(serverResponse);
    } else {
      closeModal();
    }
  };

  return (
    <div className="modal-signup-form">
      <h1>Sign Up</h1>
      {errors.server && <p className="error">{errors.server}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Email
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        {errors.email && <p className="error">{errors.email}</p>}
        <label>
          Username
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        {errors.username && <p className="error">{errors.username}</p>}
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        {errors.password && <p className="error">{errors.password}</p>}
        <label>
          Confirm Password
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </label>
        {errors.confirmPassword && <p className="error">{errors.confirmPassword}</p>}
        <label>
          About Me:
          <textarea
            value={aboutMe}
            onChange={(e) => setAboutMe(e.target.value)}
            required
          />
        </label>
        {errors.user_about && <p className="error">{errors.user_about}</p>}

        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default SignupFormModal;
