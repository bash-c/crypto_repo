void __fastcall check(_BYTE *in, __int64 len)
{
  int v2; // edx@2
  bool v3; // zf@2
  __int64 v4; // rcx@2
  _BYTE *st; // rax@3
  _BYTE *ed; // rsi@3
  int v7; // er8@4

  if ( len )
  {
    /* v2 = n1 + *in; */
	v2 = in[n1]
    v4 = (n2 + 1);
    n1 += in[0];
    ++n2;
    if (in[n1] != data[n2] )
    {
      puts("Bad flag :(");
      exit(1);
    }
    /* st = in + 1; */
	st = &in[1];
    ed = &in[len];
    while ( st != ed )
    {
      v7 = *st++;
      v2 += v7;
      n1 = v2;
      n2 = v4 + 1;
      if ( v2 != data[v4] )
		  exit(1);
	  v4++;
    }
  }
}
