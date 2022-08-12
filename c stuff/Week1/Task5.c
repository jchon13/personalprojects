#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void){
    srand(time(NULL));

    int i;

    for(i = 0; i<6;++i){
        printf("%d\n",rand());
    }
    return 0;
}