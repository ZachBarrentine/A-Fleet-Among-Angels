import '../css/Home.css'
import {Link} from "react-router-dom";

function Home(){
    return ( 
    <>
        
        <div className="TitleBox">
            <h1 className="homeTitle">A Fleet Among Angels</h1>
            <p className="homeSubtitle">Rebirth of a Galactic Peril</p>
        </div>
        <div className="homeContainer">
            <br/>
            <p className="subtitle">A new tactical SRPG forging its path among the stars!</p>
            <br/>
            <p className="bodyContent">Welcome to the official website for A Fleet Among Angels: a browser-based Tactical Strategy Role-Playing Game currently in active development! <br/><br/>
                                Here you can find our active development progress, learn more about our project, and try out our playable demo.
            </p>
        <Link to ="/Demo" className="playButton">PLAY DEMO</Link>
        </div>
    </>    
    );
}

export default Home;