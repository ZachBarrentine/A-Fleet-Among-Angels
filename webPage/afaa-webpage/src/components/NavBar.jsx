import {Link} from "react-router-dom";
import "../css/NavBar.css";

function NavBar(){
    return (
    <nav className="navbar">
        <div className="navbarLinks">
            <Link to ="/" className="navLink">Home</Link>
            <Link to ="/AboutTheProject" className="navLink">About</Link>
            <Link to ="/Progress" className="navLink">Progress</Link>
        </div>
        <div className="navbarLinks">
            <Link to ="/Progress" className="navDemo">Demo</Link>
        </div>
    </nav>
    );
}

export default NavBar;