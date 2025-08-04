#include <stdio.h>
#include "func.h"

int main(void){
    int array[4] = {1,4,3,1};
    int length = 4;

    printf("The largest element is at %d with a value of %d", find_largest(array,length),*find_largest(array,length));

    return 0;
}