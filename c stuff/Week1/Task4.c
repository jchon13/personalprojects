#include <stdio.h>

int main(void)
{
    char num[4];
    
    printf("Enter a four digit number: ");
    scanf("%s", &num);

    printf("%c%c%c%c",num[3],num[2],num[1],num[0]);

    return 0;
}