int main()
{
    int a= 0;
    int b= a;
    int c = b;
    char buf[7];
    char buf2[7];
    buf2[0] = 10;
    int * bleed = (int *)(&buf[6]);
    *bleed = c;
    int x = 10/buf2[0];
    return 0;
}