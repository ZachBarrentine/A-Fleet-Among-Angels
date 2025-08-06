import "../css/Demo.css"
import {auth} from '../../firebase'
import { useAuthState } from 'react-firebase-hooks/auth'; // need to install using npm install react-firebase-hooks
import {signOut} from "firebase/auth";
import {Link} from "react-router-dom";

function Demo(){
    
    const [user] = useAuthState(auth);
    
    return (
        <div>
            <h1 className ="projectHeadline">Demo Placeholder</h1>
            <ul className="DemoBody">
            Placeholder line above the demo screen. The screen will lead into the login/user auth and then the main menu.
            </ul>
            <div className="demoScreen">
                <h1 className="demoTitle">Demo</h1>
                <div className="demoScreen">
                </div>
            </div>
            <div className = "signNplay">
            <button className="playDemoButton">PLAY DEMO</button>
            {user ? <SignOut /> : <Link to = "/SignIn" className = "signInButton">Sign In</Link>}
            </div>
        </div>
    );
}

function SignOut(){
    return (<button className="signOutButton" onClick={() => signOut(auth).catch((error) => {
        console.error("Failed to sign out:", error)})}>Sign Out</button>)
}

export default Demo;