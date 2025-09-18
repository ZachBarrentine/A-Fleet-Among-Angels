import {Link} from "react-router-dom";
import "../css/NavBar.css";

function NavBar(){
    return (
    <nav className="navbar">
        <div className="navbarLinks">
            <Link to ="/" className="navLink2">Home</Link>
            <Link to ="/AboutTheProject" className="navLink">About</Link>
            <Link to ="/Progress" className="navLink">Progress</Link>
        </div>
        <div className="navLogo">
        </div>
        <div className="navbarLinks">
            <Link to ="/Demo" className="navDemo">PLAY DEMO</Link>
        </div>
    </nav>
    );
}

export default NavBar;