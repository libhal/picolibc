#include <cstdio>

int
main()
{
  int a = 5;
  fprintf(stdout, "a = %d\n", a);
  return 0;
}

extern "C"
{
  struct _reent* _impure_ptr = nullptr;
}