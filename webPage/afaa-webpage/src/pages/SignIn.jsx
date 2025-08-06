import {auth} from '../../firebase'
import { useState } from 'react';
import { GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword } from "firebase/auth";
import { Link } from "react-router-dom";
import { useNavigate } from 'react-router-dom';
import "../css/SignIn.css"

function SignInPage(){
    
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSignIn = async (e) => {
        
        e.preventDefault();
    
        try{
            await signInWithEmailAndPassword(auth, email, password)
            navigate('/Demo');
        }
        catch(error){
            if(error.code === 'auth/user-not-found'){
                alert("email / user not found.");
            }
            else if(error.code === 'auth/wrong-password'){
                alert("Incorrect password.");
            }
            else if(error.code === 'auth/invalid-credential'){
                alert("Incorrect email or password");
            }
            else{
                alert("Failed to sign in:" + error.message);
            }
        };
      }
    
    return (
        <div className='mainBox'>
        <div className='signInBox'>
            <h1 className ="signInTitle">A Fleet Among Angels</h1>
            
            <form onSubmit = {handleSignIn}>

            <input type="email"
                   className="email"
                   placeholder="Email"
                   value={email}
                   onChange={(e) => setEmail(e.target.value)}
                   required/>
            
            <br></br>
            
            <input type="password" 
                   className="password"
                   placeholder='Password'
                   value={password}
                   onChange={(e) => setPassword(e.target.value)}
                   required/>

            <button type='submit'
                   className='submit'>Sign In</button>

            </form>

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

export default SignInPage;