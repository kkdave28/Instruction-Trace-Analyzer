#include "stdlib.h"
#include "stdio.h"
#include "string.h"
int main(int argc, char const * argv[])
{
    char buf[8], buf2[8];
    buf2[0] = 'x';
    buf2[1] = 'x';
    buf2[2] = 'x';
    int * bleed = (int *)(&buf[7]);
    *bleed = 0; // taint assumed here.
    int crashing_stuff= 123/buf2[0];
    return 0;
}