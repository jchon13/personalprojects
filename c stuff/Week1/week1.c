/*Multiple Line
Comments*/

//single line

#include<stdio.h>

int main()
{
    printf("Welcome to C Programming!\n");
    return 0;
}

//constants
#define MAX_LENGTH 9

//variables
int i=0, j=1, k = 2;
float pi = 3.1415926553f;
double e = 1.0e-32;
char c = 'a';
char newline = '\n';

/*

Data Types in order of size

Integer: Char (1), Short (2), Int (4), Long (8), Long Long(8)
Floating Point: float, double, long double

Single quotation marks represent character code of that character
Double qoutation marks are used for string literals 
(Follow with a null character \0)

*/

//arrays
int a[10];
a[2] = 3; /*initialise third element of a 10 element array*/

char unit_code[MAX_LENGTH]; /*string with 9 characters*/
char unit_name[] = "OS"; /*length 3 including \0*/


//functions and prototypes

int foo(int a, int b)
{
    /*code*/
    return 0;
}

//prototypes
int foo(int a, int b);


//to run type: hello.c -o hello