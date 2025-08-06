import {auth} from '../../firebase'
import { useState } from 'react';
import { createUserWithEmailAndPassword, validatePassword } from "firebase/auth";
import { useNavigate } from 'react-router-dom';
import "../css/SignUp.css"

function SignUpWithUAndP(){
   
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSignUp = async (e) => {
    
        e.preventDefault();

        const status = await validatePassword(auth, password);

        if(!status.isValid){
            alert("Password must contain an uppercase letter and a special character (_, /, -).");
            return
        }

        try{
            await createUserWithEmailAndPassword(auth, email, password)
            navigate('/Demo');
        }
        catch(error){
            console.error(error.message);
        };
    }
  
    return (
        <div className='mainUpBox'>
        <div className='signUpBox'>
            <h1 className ="signUpTitle">A Fleet Among Angels</h1>
            
            <form onSubmit={handleSignUp}>

            <input type="email"
                   value={email}
                   className="emailUp"
                   placeholder="Email"
                   onChange={(e) => setEmail(e.target.value)}
                   required/>
            
            <br></br>
            
            <input type="password" 
                   value={password}
                   className="passwordUp"
                   placeholder='Password'
                   onChange={(e) => setPassword(e.target.value)}
                   required/>

            <br></br>

            <button 
                   type='submit'
                   className='submitUp'>Sign Up</button>
            </form>
        </div>
        </div>
    );
}

export default SignUpWithUAndP;