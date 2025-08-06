import {Routes, Route} from 'react-router-dom'
import { useLocation } from 'react-router-dom'
import './css/App.css'
import NavBar from './components/NavBar'
import AboutTheProject from './pages/AboutTheProject'
import Progress from './pages/Progress'
import Home from './pages/Home'
import Demo from './pages/Demo'
import SignInPage from './pages/SignIn.jsx'
import SignUpPage from './pages/SignUp.jsx'
import '../firebase.js'


function App() {
  const location = useLocation();
  const hideNavBar = ['/SignIn', '/SignUp'];

  return (
    <>
      {!hideNavBar.includes(location.pathname) && <NavBar />}   
      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/AboutTheProject" element={<AboutTheProject />}></Route>
        <Route path="/Progress" element={<Progress />}></Route>
        <Route path="/Demo" element={<Demo />}></Route>
        <Route path="/SignIn" element={<SignInPage />}></Route>
        <Route path="/SignUp" element={<SignUpPage />}></Route>
      </Routes>
    </>
  );
}

export default App;
