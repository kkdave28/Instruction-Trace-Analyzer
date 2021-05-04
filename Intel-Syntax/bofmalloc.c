#include <stdlib.h>
int test(int a, int b, int c, int d, int e, int f, int h, int i, int j, int k, int l, int m, int n)
{
    int g = a+b+c+d+e+f+h+i+j+k+l+m+n;
    return g;
}
int main()
{
    int x = test(1,2,3,4,5,6,7,8,9,1,2,3,4);
    return x;
}