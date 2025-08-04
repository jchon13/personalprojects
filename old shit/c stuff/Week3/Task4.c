#include <stdio.h>
#include <string.h>




int main(void){

    struct UnitCode{
    char *FacID;          
    int UnitID; 
    } unit1,unit2;

    unit1.FacID = "FIT";
    unit1.UnitID = 1047;

    unit2.FacID = "FIT";
    unit2.UnitID = 1047;

    if(strcmp(unit1.FacID,unit2.FacID)==0 && unit1.UnitID==unit2.UnitID){
        printf("Both Instances are the same");
    }
    else{
        printf("They are different");
    }
    return 0;
}

