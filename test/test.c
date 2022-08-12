#include <stdio.h>

int *foo(int arg1[], int arg2){
    int *total;
    int sum = 0;
    for (int i=0; i<arg2; i++){
        sum = sum + arg1[i];
        
    }
    total = &sum;
    return total;
}

int main(void){
    int vo[4] ={1,2,3,4};
    int length = 4;

    int total = 0;

    printf("%d",*foo(vo,length));
}