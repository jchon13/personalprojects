const cellElements = document.querySelectorAll('[data-cell]');
const board = document.getElementById('board');
cellElements.forEach( cell => {
    cell.addEventListener('click',handleClick,{once:true})
});
const restart = document.getElementById('restartButton');
restart.addEventListener('click',restart_func);
const WINNING_COMBINATIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];

const winScreen = document.getElementById('winningMessage')
winScreen.className = 'winning-message';

const winMessage = document.querySelector('[data-winning-message-text]')

let currentTurn = 'x'; //true is x
swapHover();

function handleClick(e) {
    //places mark
    const cell = e.target;
    if (currentTurn === 'x')
    {
        cell.classList.add('x');
        if (checkWin(currentTurn))
        {
            console.log('yes');
            winScreen.className = 'winning-message show';
            winMessage.innerText = 'X\'s wins!';
        }
        currentTurn = 'circle';
    }
    else
    {
        cell.classList.add('circle');
        if (checkWin(currentTurn))
        {
            console.log('yes')
            winScreen.className = 'winning-message show';
            winMessage.innerText = 'O\'s wins!';
        }
        currentTurn = 'x';
    }

    swapHover();
    //checks for win, loss, draw
}

function swapHover(){
    board.classList.remove('x');
    board.classList.remove('circle');
    if (currentTurn === 'x'){
        board.classList.add('x')
    }
    else{
        board.classList.add('circle')
    }
}

 function restart_func() 
 {
    cellElements.forEach( cell => {
        cell.className = 'cell' 
    })
    cellElements.forEach( cell => {
        cell.addEventListener('click',handleClick,{once:true})
    });
    currentTurn = 'x';
    swapHover();
    winScreen.className = 'winning-message';
};


function checkWin(currentClass) {
    return WINNING_COMBINATIONS.some(combination => {
      return combination.every(index => {
        return cellElements[index].classList.contains(currentClass)
      })
    })
  }