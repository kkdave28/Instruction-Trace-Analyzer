#include "stdlib.h"
#include "string.h"
int feed_val()
{
    return 34;
}
int main()
{
    char * buf = (char *)malloc(sizeof(char) *8);
    char * buf2 = (char *)malloc(sizeof(char) * 10);
    memset(buf, 97, sizeof(buf));
    memset(buf2, 122, sizeof(buf2));
    buf [feed_val()] = 97;
    return 0;
}