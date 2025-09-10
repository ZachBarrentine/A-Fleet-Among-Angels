import "../css/Demo.css"
import {auth} from '../../firebase'
import { useAuthState } from 'react-firebase-hooks/auth'; // need to install using npm install react-firebase-hooks
import {signOut} from "firebase/auth";
import {useNavigate} from "react-router-dom";

function Demo(){
    
    const [user] = useAuthState(auth);
    const navigate = useNavigate();
    
    return (
        <div>
            <h1 className ="projectHeadline">Demo Placeholder</h1>
            <p className="DemoBody">
            Placeholder line above the demo screen. The screen will lead into the login/user auth and then the main menu.
            </p>
            <div className="demoScreen">
                <h1 className="demoTitle">Demo</h1>
                <div className="demoScreen">
                </div>
            </div>
            <div className = "signNplay">
            <button className="playDemoButton">PLAY DEMO</button>
            {user ? <SignOut /> : <button className = "signInButton" onClick={() => navigate("/SignIn")}>Sign In</button>}
            </div>
        </div>
    );
}

function SignOut(){
    return (<button className="signOutButton" onClick={() => signOut(auth).catch((error) => {
        console.error("Failed to sign out:", error)})}>Sign Out</button>)
}

export default Demo;