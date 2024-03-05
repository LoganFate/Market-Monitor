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
