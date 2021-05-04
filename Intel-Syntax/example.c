int myAtoi(const char* str)
{
    // Initialize result
    int res = 0;
 
    // Iterate through all characters
    // of input string and update result
    // take ASCII character of corosponding digit and
    // subtract the code from '0' to get numerical
    // value and multiply res by 10 to shuffle
    // digits left to update running total
    for (int i = 0; str[i] != '\0'; ++i)
        res = res * 10 + str[i] - '0';
 
    // return result.
    return res;
}
int main(int argc, char const * argv[])
{
    int a= 0;
    int b= a;
    int c = b;
    char buf[7];
    char buf2[7];
    buf2[0] = 10;
    int * bleed = (int *)(&buf[6]);
    int val = myAtoi(argv[1]);
    char q = 'x';
    *bleed = val;
    char y = 'y';
    int x = 10/buf2[0];
    return 0;
}