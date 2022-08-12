#include <stdio.h>
#include "func.h"

int main(void)
{
    int num1,num2;
    printf("Enter two numbers:");
    scanf("%d %d",&num1,&num2);

    
    printf("Addtion = %d\n",add(num1,num2));

    
    printf("Subtraction = %d\n",sub(num1,num2));

    
    printf("Multiplication = %d\n",mult(num1,num2));

    
    printf("Division = %d\n",div(num1,num2));


    return 0;
}

//gcc -o my_app main.c foo.c