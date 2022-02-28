function powerOfThree(number) {
    if(number < 0)
    {
        return false;
    }

    while(number % 3 === 0)
    {
        number = number/3;
        console.log(number);
    }

    return number ===1;
}

console.log(powerOfThree(9));