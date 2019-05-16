
var problemBoard 

function generateBoard(difficulty) {
    
    problemBoard = [
        [2, 8, 6, 7, 5, 4, 9, 3, 1],
        [9, 3, 1, 2, 8, 6, 7, 5, 4],
        [7, 5, 4, 9, 1, 3, 8, 6, 2],
        [8, 9, 2, 6, 7, 5, 4, 1, 3],
        [6, 7, 5, 4, 3, 1, 2, 9, 8],
        [4, 1, 3, 8, 9, 2, 6, 7, 5],
        [5, 6, 9, 3, 4, 8, 1, 2, 7],
        [3, 4, 7, 1, 2, 9, 5, 8, 6],
        [1, 2, 8, 5, 6, 7, 3, 4, 9]
    ];
    let random10 = Math.floor((Math.random() * 10) + 1);
    for (let r = 0; r < random10; r++) {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                problemBoard[i][j] = problemBoard[i][j] + 1;
                if (problemBoard[i][j] == 10) {
                    problemBoard[i][j] = 1;
                }
            }
        }
    }
    let min = difficulty;
    let max = min + 2;
    problemBoard.forEach((row) => {
        let toReplace = shuffleArray([0, 1, 2, 3, 4, 5, 6, 7, 8]);
        for (let i = 0; i < Math.floor(Math.random() * (max - min + 1) + min); i++) {
            row[toReplace[i]] = 0;
        }
    });
    renderBoard(problemBoard);
    
    $.post("/problem_submission", {"javascript_data" : JSON.stringify(problemBoard)})
  
}

function generateSolution(){

    $.get("/solution_request", function(d){

        var JSONObject = JSON.parse(d);
        var solution = JSONObject.solution
        var correctnessTable = [
        [false,false,false,false,false,false,false,false,false],
        [false,false,false,false,false,false,false,false,false],
        [false,false,false,false,false,false,false,false,false],
        [false,false,false,false,false,false,false,false,false],
        [false,false,false,false,false,false,false,false,false],
        [false,false,false,false,false,false,false,false,false],
        [false,false,false,false,false,false,false,false,false],
        [false,false,false,false,false,false,false,false,false],
        [false,false,false,false,false,false,false,false,false]
        ]
        
        console.log("solution " + solution)

        for (let i = 0; i < 9; i++){
            for (let j = 0; j < 9; j++){
                el = document.getElementById(i + " " + j)
                n = el.getElementsByClassName("num")[0]
                
                if (n.innerHTML === solution[i][j].toString()){
                    correctnessTable[i][j]=true
                }
                else{
                    correctnessTable[i][j]=false
                }
            }
        }

        renderBoard(solution, correctnessTable)

   })}


function renderBoard(boardToRender, correctnessTable) {

    let board = boardToRender;
    let html = '';
    for (let i = 0; i < 9; i++) {
        html += "<div class='row' >";
        for (let j = 0; j < 9; j++) {

            // if (i == 2 && j == 2) {
            //     html += "            <div class='box border-right border-bottom '  >";
            // } else if (j == 2 || j == 5) {
            //     html += "            <div class='box border-right'  >";

            if ((i == 2 && j == 2) || (i == 2 && j == 5) || (i == 5 && j == 2) || (i == 5 && j == 5)) {
                html += "            <div class='box border-right border-bottom ' id = '" + i + " " + j  + "'>";
            } else if (i == 2 || i == 5) {
                html += "            <div class='box border-bottom'  id = '" + i + " " + j  + "'>";
            } else if (j == 2 || j == 5) {
                html += "            <div class='box border-right'  id = '" + i + " " + j  + "'>";
            } else {
                html += "            <div class='box'  id = '" + i + " " + j  + "'>";
            }

            if (correctnessTable === undefined){
                if (board[i][j] == 0) {
                    html += "                <div class = 'empty'>"
                } else {
                    html += "                <div class='fixed'  >"
                }
            }
            else{
                 if (correctnessTable[i][j] == false) {
                    html += "                <div class = 'wrong'>"
                } else {
                    html += "                <div class='right'  >"
                }
            }

            if (board[i][j] == 0){
                html += "                    <div class = 'num' id = 'input' contenteditable>" + '' + "</div>"
            }
            else{
                html += "                    <div class = 'num'>" + board[i][j] + "</div>"
            }
            html += "                </div>"
            html += "            </div>"
        }
        html += "        </div>"

    }
    document.getElementsByClassName('board')[0].innerHTML = html;

}
// -------SHUFFLE ARRAY------------
function shuffleArray(array) {
    let currentIndex = array.length,
        temporaryValue, randomIndex;
    // While there remain elements to shuffle inside the array
    while (0 !== currentIndex) {
        // Pick a remaining element from the array
        randomIndex = Math.floor(Math.random() * currentIndex);
        // randomIndex is a random number between 0 and the array position
        currentIndex -= 1;
        // We get a new currentIndex and swap it with the current element.
        temporaryValue = array[currentIndex];
        // We save the currentIndex value in temporaryValue
        array[currentIndex] = array[randomIndex];
        // Now we fill the new currentIndex position with the value from the randomIndex
        array[randomIndex] = temporaryValue;
        // Lastly in the randomIndex position we put the temporaryValue we saved before
    }
    return array;
}