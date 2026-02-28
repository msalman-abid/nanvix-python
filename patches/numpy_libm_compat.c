#include <math.h>

long double __kernel_tanl(long double x, long double y, int iy)
{
    (void)y;
    (void)iy;
    return (long double)tan((double)x);
}
