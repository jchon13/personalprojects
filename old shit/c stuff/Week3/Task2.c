#include <stdio.h>
#include <stdlib.h>

int main(void){
    int n;
    int total = 0;

    printf("Enter length of series:");
    scanf("%d",&n);

    int *ptr = (int*) malloc(sizeof(int)*n);

    printf("Enter %d numbers (one by one): \n", n);
    for(int i=0; i<n; i++){
        scanf("%d",&ptr[i]);
        total = total + ptr[i];
    }

    printf("Sum of all elements = %d",total);

    free(ptr);

    return 0;

}