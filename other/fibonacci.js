//returns a number in the fibonacci sequence from two starting numbers.

function fibonacci(n,number1,number2) {
    let fib=[number1,number2];
    if(n<0 || n>30)
    {
        return null;
    }
    while(n > fib.length)
    {
        fib[fib.length]= fib[fib.length-1]+fib[fib.length-2];
    }
    console.log(fib[n-1]);
}

fibonacci(8,1,1)