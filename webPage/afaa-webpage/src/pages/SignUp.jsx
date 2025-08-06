import {auth} from '../../firebase'
import { useAuthState } from 'react-firebase-hooks/auth'; // need to install using npm install react-firebase-hooks
import { signInWithEmailAndPassword } from "firebase/auth";
import { Link } from "react-router-dom";
import "../css/SignUp.css"

function SignInPage(){
    
    const [user] = useAuthState(auth);
    
    return (
        <div className='mainUpBox'>
        <div className='signUpBox'>
            <h1 className ="signUpTitle">A Fleet Among Angels</h1>
            
            <form>

            <input type="email"
                   className="emailUp"
                   placeholder="Email"
                   required/>
            
            <br></br>
            
            <input type="password" 
                   className="passwordUp"
                   placeholder='Password'
                   required/>

            <br></br>

            <button type='submit'
                   className='submitUp'>Sign Up</button>
            </form>
        </div>
        </div>
    );
}

function SignInWithUAndP(){
    return <button className="signInButton">Sign In With Username And Password</button>
}

export default SignInPage;