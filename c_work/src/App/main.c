#include <stdio.h>
int main(){
    printf("sssss\n");

#if defined UNIT_TEST_BUILD
    printf("test\n");
#endif

    return 0;
}