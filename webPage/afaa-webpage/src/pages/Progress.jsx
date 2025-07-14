import "../css/Progress.css"

function Progress(){
    return (
    <div>
        <div className="progressBox">
        <h1 className="progressTitle">Progress & Development</h1>
        </div>
        <div className="pBodyBox">
            <p className="pBodyText"><span className="nameHighlight">A Fleet Among Angels</span> is actively under development. The game is still in the <span className="boldText">early stages</span> of development. 
            <br/><br/><br/> While there is <span className="boldText">no current progress</span> to show, here is what we are working on:
		    <br/><br/>- Establishing core gameplay mechanics (Movement, Attacks, Abilities, Etc.)
            <br/><br/>- Designing and implementing the initial set of units and their skills
            <br/><br/>- Developing the first playable levels and enemy AI to publish our demo.
            <br/><br/>- Crafting the art style and user interface.
        </p>
        </div>
    </div>
    );
}

export default Progress;