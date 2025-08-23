import "../css/Progress.css"

function Progress(){
    return (
    <div>
        <div className="progressBox">
        <h1 className="progressTitle">Progress & Development</h1>
        </div>
        <div className="pBodyBox">
            <p className="pBodyText"><span className="nameHighlight">A Fleet Among Angels</span> is actively under development. The game is still in the <span className="boldText">early stages</span> of development. 
            <br/><br/><br/> We are actively working to have the game done by the end of the year. Here is some of our progress:
		    <br/><br/>- Core gameplay mechanics: Movement and attacks have been implemented as well as the grid.
            <br/><br/>- Enemy AI has been implemented and the player can play against it.
            <br/><br/>- Health bars for both player and AI.
            <br/><br/>- Database implementation is on the works using Firebase.
        </p>
        </div>
    </div>
    );
}

export default Progress;