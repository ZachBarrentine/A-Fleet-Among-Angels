import "../css/Demo.css"
import {auth} from '../../firebase'
import { useAuthState } from 'react-firebase-hooks/auth'; // need to install using npm install react-firebase-hooks
import { GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";

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
            <button className="playDemoButton">PLAY DEMO</button>
            {user ? <SignOut /> : <SignIn />}
        </div>
    );
}

function SignIn(){
    const signInWithGoogle = () => {
        const provider = new GoogleAuthProvider();
        signInWithPopup(auth, provider).catch((error) => {
        console.error("Failed to sign in:", error)});
    }
    return <button className="signInButton" onClick={signInWithGoogle}>Sign In</button>
}

function SignOut(){
    return (<button className="signOutButton" onClick={() => signOut(auth).catch((error) => {
        console.error("Failed to sign out:", error)})}>Sign Out</button>)
}

export default Demo;