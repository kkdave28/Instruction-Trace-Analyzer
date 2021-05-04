#include "stdlib.h"
#include "stdio.h"
#include "string.h"
void another_fubar_lol(char * ptr)
{
    int * bleed = (int *)(ptr);
    *bleed = 0;
}
void fubar(char * ptr)
{
    another_fubar_lol(ptr);
}
int main(int argc, char const * argv[])
{
    char buf[8], buf2[8];
    buf2[0] = 'x';
    buf2[1] = 'x';
    buf2[2] = 'x';
    fubar(&buf[7]);
    //int * bleed = (int *)(&buf[7]);
    //*bleed = 0; // taint assumed here.
    int j = 0;
    for(; j< 10; j++)
        printf("%c", buf2[0]);
    //for(j=0; j< 10; j++)
      //  buf2[0] = 9-j;
    int crashing_stuff= 123/buf2[0];
    return 0;
}