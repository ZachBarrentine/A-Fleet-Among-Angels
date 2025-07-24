import "../css/Demo.css"

function Demo(){
    return (
        <div>
            <h1 className ="projectHeadline">Demo Placeholder</h1>
            <ul className="DemoBody">
            Placeholder line above the demo screen. The screen will lead into the login/user auth and then the main menu.
            </ul>
            <div className="demoScreen">
                <h1 className="demoTitle">Demo</h1>
                <div className="demoScreen">
                </div>
            </div>
            <button className="playButton">PLAY DEMO</button>
        </div>
    );
}

export default Demo;