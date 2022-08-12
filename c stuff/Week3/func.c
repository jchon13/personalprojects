#include "func.h"

int *find_largest(int the_array[], int num_elements){

    int *value = &the_array[0];

    for(int i=0; i<num_elements; i++){
        if (the_array[i] > *value){
            value = &the_array[i];
        }
    }

    return (value);

}