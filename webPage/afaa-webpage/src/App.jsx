import { useState } from 'react'
import {Routes, Route} from 'react-router-dom'
import './css/App.css'
import NavBar from './components/NavBar'
import AboutTheProject from './pages/AboutTheProject'
import Progress from './pages/Progress'
import Home from './pages/Home'

function App() {
  //const [count, setCount] = useState(0)
  return (
    <>
      <NavBar />      
      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/AboutTheProject" element={<AboutTheProject />}></Route>
        <Route path="/Progress" element={<Progress />}></Route>
      </Routes>
    </>
  );
}

export default App;
