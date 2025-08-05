import "../css/Demo.css"
import {auth} from '../../firebase'
import { useAuthState } from 'react-firebase-hooks/auth'; // need to install using npm install react-firebase-hooks
import { GoogleAuthProvider, signInWithPopup, signOut, signInWithEmailAndPassword } from "firebase/auth";

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
            {user ? (<div className = "demoSignOut"><button className="playDemoButton">PLAY DEMO</button><SignOut /> </div>) : 
                    ( <><SignInWithG /> <button className="playDemoButton">PLAY DEMO</button> <SignInWithUAndP /> </>)}
            </div>
        </div>
    );
}

function SignInWithG(){
    const signInWithGoogle = () => {
        const provider = new GoogleAuthProvider();
        signInWithPopup(auth, provider).catch((error) => {
        console.error("Failed to sign in:", error)});
    }
    return <button className="signInGButton" onClick={signInWithGoogle}>Sign In With Google</button>
}

function SignInWithUAndP(){
    // Placeholder for future un and pw sign-in
    return <button className="signInButton">Sign In With Username And Password</button>
}

function SignOut(){
    return (<button className="signOutButton" onClick={() => signOut(auth).catch((error) => {
        console.error("Failed to sign out:", error)})}>Sign Out</button>)
}

export default Demo;