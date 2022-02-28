const buttonElements = document.querySelectorAll('[buttons]');
buttonElements.forEach( button => {
    button.addEventListener('click',clickHandle)
});

const equals = document.getElementById('equal');
equals.addEventListener('click',calculateValue);

const clear = document.getElementById('clear');
clear.addEventListener('click',clearCalculator);

const backSpace = document.getElementById('delete');
backSpace.addEventListener('click',deletePrev);

let calculated = false;

function clickHandle(e) {
    const button = e.target;
    if (calculated === true) {
        if(button.innerText == '+' || button.innerText == '-' || button.innerText == '*' || button.innerText == '/')
        {
            let value = display.innerText;
            value = value + button.innerText;
            display.innerText = value;
            calculated = false;
        }
        else{
            display.innerText = button.innerText;
            calculated = false;
        }

    }
    else
    {
        let value = display.innerText;
        value = value + button.innerText;
        display.innerText = value;
    }
}

function calculateValue(){
    let value = display.innerText;
    display.innerText = eval(value);
    console.log(eval(value));
    calculated = true;
}

function clearCalculator(){
    calculated = false;
    display.innerText = '';
}

function deletePrev(){
    let value = display.innerText;
    display.innerText = value.substring(0, value.length -1);
}
