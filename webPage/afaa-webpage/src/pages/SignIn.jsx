import {auth} from '../../firebase'
import { useAuthState } from 'react-firebase-hooks/auth'; // need to install using npm install react-firebase-hooks
import { GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword } from "firebase/auth";
import { Link } from "react-router-dom";
import { useNavigate } from 'react-router-dom';
import "../css/SignIn.css"

function SignInPage(){
    
    const [user] = useAuthState(auth);
    
    return (
        <div className='mainBox'>
        <div className='signInBox'>
            <h1 className ="signInTitle">A Fleet Among Angels</h1>
            
            <form>

            <input type="email"
                   className="email"
                   placeholder="Email"
                   required/>
            
            <br></br>
            
            <input type="password" 
                   className="password"
                   placeholder='Password'
                   required/>

            </form>

            <button type='submit'
                   className='submit'>Sign In</button>


            <p className="or">or</p>

            <SignInWithG />
            <Link to ="/SignUp" className='signUp'>Don't have an account? Sign Up</Link>
        </div>
        </div>
    );
}

function SignInWithG(){
    const navigate = useNavigate();
    const signInWithGoogle = async () => {
        const provider = new GoogleAuthProvider();
        try{
            await signInWithPopup(auth, provider);
            navigate('/Demo');
        }
        catch(error){
        console.error("Failed to sign in:", error)};
    }
    return <button className="signInGButton" onClick={signInWithGoogle}>Sign In With Google</button>
}

function SignInWithUAndP(){
    return <button className="signInButton">Sign In With Username And Password</button>
}

export default SignInPage;