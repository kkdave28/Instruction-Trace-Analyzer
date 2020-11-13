#include "stdlib.h"
int main(int argc, char const * argv[])
{
    int i = atoi(argv[1]);
    int index = i+1;
    char buf [8];
    buf[index] = 'x';
    return 0;
}