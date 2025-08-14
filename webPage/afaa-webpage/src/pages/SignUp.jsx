import { auth } from '../../firebase'
import { useState } from 'react';
import { createUserWithEmailAndPassword } from "firebase/auth";
import { useNavigate } from 'react-router-dom';
import "../css/SignUp.css"

function SignUpWithUAndP() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [hasUppercase, setHasUppercase] = useState(false);
    const [hasSpecial, setHasSpecial] = useState(false);
    const [hasMinLength, setHasMinLength] = useState(false);

    const validatePassword = (pwd) => {
        const uppercaseCheck = /[A-Z]/.test(pwd);
        const specialCheck = /[_\/\-!\?\*]/.test(pwd);
        const lengthCheck = pwd.length >= 8 && pwd.length <= 20;

        setHasUppercase(uppercaseCheck);
        setHasSpecial(specialCheck);
        setHasMinLength(lengthCheck);

        return uppercaseCheck && specialCheck && lengthCheck;
    };

    const handlePasswordChange = (e) => {
        const value = e.target.value;
        setPassword(value);
        validatePassword(value);
    };

    const handleSignUp = async (e) => {
        e.preventDefault();

        if (!(hasUppercase && hasSpecial && hasMinLength)) {
            return;
        }

        try {
            await createUserWithEmailAndPassword(auth, email, password);
            navigate('/Demo');
        } catch (error) {
            console.error(error.message);
        }
    };

    const isPasswordValid = hasUppercase && hasSpecial && hasMinLength;

    return (
        <div className='mainUpBox'>
            <div className='signUpBox'>
                <h1 className="signUpTitle">A Fleet Among Angels</h1>

                <form onSubmit={handleSignUp}>
                    <input
                        type="email"
                        value={email}
                        className="emailUp"
                        placeholder="Email"
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <br />

                    <input
                        type="password"
                        value={password}
                        className={`passwordUp ${!isPasswordValid && password.length > 0 ? 'invalid' : ''}`}
                        placeholder='Password'
                        onChange={handlePasswordChange}
                        required
                    />
                    <br />

                    {/* Giving properties for all three checkers based on whether reqs were filled */}
                    <div className='passwordStrength' style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', marginTop: '10px' }}>
                        <div style={{ color: hasUppercase ? 'green' : 'red', fontWeight: hasUppercase ? 'normal' : 'bold' }}>
                            {hasUppercase ? "✅" : "❌"} At least 1 uppercase letter
                        </div>
                        <div style={{ color: hasSpecial ? 'green' : 'red', fontWeight: hasSpecial ? 'normal' : 'bold' }}>
                            {hasSpecial ? "✅" : "❌"} At least 1 special character (_, /, -, !, ?, *)
                        </div>
                        <div style={{ color: hasMinLength ? 'green' : 'red', fontWeight: hasMinLength ? 'normal' : 'bold' }}>
                            {hasMinLength ? "✅" : "❌"} Between 8 and 20 characters
                        </div>
                    </div>

                    <button
                        type='submit'
                        className='submitUp'
                        disabled={!isPasswordValid}
                    >
                        Sign Up
                    </button>
                </form>
            </div>
        </div>
    );
}

export default SignUpWithUAndP;
