import { NavLink, Link } from "react-router-dom";
import logoImg from '/MarketMonitorLogo.jpg';
import "./Navigation.css";

function Navigation({ isLoggedIn }) { // Pass isLoggedIn as a prop
  return (
    <nav>

      <div className="logo">
        <NavLink to="/">
          <img src={logoImg} alt="Market-Monitor Logo" />
          </NavLink>
          <span className="logo-text">Market Monitor</span>
          </div>

      <ul className="nav-links">
        {!isLoggedIn && ( // Show these links if the user is NOT logged in
          <>
            <li><Link to="/login" className="button">Login</Link></li>
            <li><Link to="/signup" className="button">Signup</Link></li>
          </>
        )}
        {isLoggedIn && ( // Show these links if the user IS logged in
          <>
            <li><Link to="/profile" className="button">Profile</Link></li>
            <li><Link to="/home" className="button">Home</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Navigation;
