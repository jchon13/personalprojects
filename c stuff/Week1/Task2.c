#include <stdio.h>

int main(void)
{
    int radius;
    #define pi 3.14159265

    printf("Enter a radius: ");
    scanf("%d", &radius);

    int vol = 4*pi*radius*radius*radius/3;
    int sa = 4*pi*radius*radius;

    
    printf("Volume: %d, Surface Area: %d",vol,sa);

    return 0;


}