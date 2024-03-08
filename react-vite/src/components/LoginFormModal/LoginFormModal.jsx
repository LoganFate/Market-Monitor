import { useNavigate } from 'react-router-dom';
import { useState } from "react";
import { thunkLogin } from "../../redux/session";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import "./LoginForm.css";

function LoginFormModal() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const { closeModal } = useModal();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const serverResponse = await dispatch(thunkLogin({ email, password }));

    if (serverResponse) {
      setErrors(serverResponse);
    } else {
      closeModal();
      navigate('/home');
    }
  };

  const handleDemoLogin = async () => {
    const demoEmail = 'demo1@example.com';
    const demoPassword = 'password1';

    const serverResponse = await dispatch(thunkLogin({ email: demoEmail, password: demoPassword }))

    if (!serverResponse) {
      closeModal();
      navigate('/home');
    } else {
      console.error("Demo Login Failed")
  }
};

  return (

      <div className="modal-login-form">
        <h1>Log In</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
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
          </div>
          <div className="form-group">
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
          </div>
          <button type="submit" className="login-button">Log In</button>
          <button type="button" onClick={handleDemoLogin} className="login-button">Demo User Log In</button>
          <div className="form-footer">
            <p>
              Don&apos;t have an account? <a href="/signup">Create one</a>
            </p>
          </div>
        </form>
      </div>
    );
  }

export default LoginFormModal;
