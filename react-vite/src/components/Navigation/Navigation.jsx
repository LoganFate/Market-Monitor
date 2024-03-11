import { NavLink, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux';
import logoImg from '/MarketMonitorLogo.jpg';
import { useModal } from "../../context/Modal";
import LoginFormModal from '../LoginFormModal';
import SignupFormModal from "../SignupFormModal"
import { thunkLogout } from "../../redux/session";
import "./Navigation.css";

function Navigation() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { setModalContent } = useModal();
  const user = useSelector(state => state.session.user);


  const openLoginModal = () => {
    setModalContent(<LoginFormModal />);
  };

  const openSignupModal = () => {
    setModalContent(<SignupFormModal />);
  };

  const handleLogout = () => {
    dispatch(thunkLogout()).then(() => {
      navigate("/");
    });
  };


  return (
    <nav>

      <div className="logo">
        <NavLink to="/">
          <img src={logoImg} alt="Market-Monitor Logo" />
          </NavLink>
          <span className="logo-text">Market Monitor</span>
          </div>

      <ul className="nav-links">
        {!user && (
          <>
             <button onClick={openLoginModal} className="button">Login</button>
             <li><button onClick={openSignupModal} className="button">Signup</button></li>
          </>
        )}
        {user && (
          <>
          <button onClick={() => navigate("/home")} className="button">Home</button>
             <button onClick={() => navigate("/profile")} className="button">Profile</button>
             <button onClick={() => navigate("/watchlist")} className="button">Watchlist</button>
            <button onClick={handleLogout} className="button">Logout</button>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Navigation;
