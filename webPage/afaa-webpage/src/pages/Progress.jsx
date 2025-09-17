import "../css/Progress.css"

function Progress(){
    return (
    <div>
        <div className="progressBox">
        <h1 className="progressTitle">Progress & Development</h1>
        </div>
        <div className="pBodyBox">
            <p className="pBodyText"><span className="nameHighlight">A Fleet Among Angels</span> is actively under development. The game is still in the <span className="boldText">early stages</span> of development. 
            <br/><br/><br/> *We are actively working to have the game done by the end of the year. Here is some of our progress:
		    <br/><br/>- Core gameplay mechanics: Movement and attacks have been implemented as well as the grid.
            <br/><br/>- Enemy AI has been implemented and the player can play against it.
            <br/><br/>- Health bars for both player and AI.
            <br/><br/>- Database implementation is on the works using Firebase.
        </p>
        <br/><br/>
                <span className="recordTitle">Record of Changes</span>
                <p className="pBodyText">
                <span className="monthTitle">August:</span>
            </p>
                <p className="centerAlign">-- Space hub that serves as the Main Menu --</p>
        </div>
        <div className="conceptBackground1"></div>
                    <br/><br/><p className="centerAlign">-- Character concept art and backstory creation --</p>
        <div className="conceptCharacters1"></div>
    </div>
    );
}

export default Progress;