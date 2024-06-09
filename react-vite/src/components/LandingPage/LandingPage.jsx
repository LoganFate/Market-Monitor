import './LandingPage.css';
import  SignupFormModal  from '../SignupFormModal';// Import your SignupFormModal component
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom'
import { thunkLogin } from '../../redux/session';
import { useModal } from "../../context/Modal"; // Import the useModal hook
import { useEffect } from "react";

const LandingPage = () => {
    const { setModalContent } = useModal();
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleSignup = () => {
        setModalContent(<SignupFormModal />);
      };




      const handleDemoLogin = async () => {
        const demoEmail = 'demo1@example.com';
        const demoPassword = 'password1';



        const serverResponse = await dispatch(thunkLogin({ email: demoEmail, password: demoPassword }));

        if (!serverResponse) {
          navigate('/home');
        } else {
          console.error("Demo Login Failed");
        }
      };

    return (
        <div>
            <header className="about-section">
                <h1>About Market-Monitor</h1>
                <p>Market-Monitor provides you the ability to plan, track, and research stock movement in real time to develop intelligent and calculated trading strategies that you feel confident about.</p>
                <button onClick={handleDemoLogin} className="signup-button">Demo User</button>
            </header>
            <section className="features-section">
                <div className="feature">
                    <h2>Smooth Navigation</h2>
                    <p>Our in depth user profile experience allows you to add stocks and pin articles to your profile, as well as categorize them! No more hopping back and forth from page to page, or having to keep multiple tabs open.</p>
                </div>
                <div className="feature">
                    <h2>Plan your strategy</h2>
                    <p>Utilize the planner page in your profile to set yourself Daily, Weekly, Monthly, and Yearly goals to keep track of your progress AND to make sure you never miss out on a lucrative trade.</p>
                </div>
                <div className="feature">
                    <h2>Notes and Comments</h2>
                    <p>You can leave research notes and comments on corresponding stocks and articles to have easy to view information on your profile page. So dump the pen and paper, because strategizing your trading techniques just got even easier. </p>
                </div>
            </section>
            {/* More sections go here */}
        </div>
    );
};

export default LandingPage;
