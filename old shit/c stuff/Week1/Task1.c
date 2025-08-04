#include<stdio.h>

int main(void)
{
    char first[20], last[20];
    printf("Enter your first and last name: ");
    scanf("%s %s", &first,&last);

    

    printf("%c.%c",first[0],last[0]);

    return 0;
}