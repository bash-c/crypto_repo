int __fastcall cipher(FILE *a1, FILE *a2, char *passwordAddr, int a4)
{
  FILE *input; // r15@1
  FILE *output; // r13@1
  int mode; // er14@1
  signed __int64 key; // rbx@1
  char v8; // di@2
  __int64 v9; // rax@3
  signed __int64 v10; // rax@6
  unsigned __int64 v11; // rbp@8
  unsigned __int8 out; // cl@9
  __int64 v13; // rax@10
  unsigned __int8 v14; // si@14
  int result; // eax@17
  unsigned __int8 v16; // si@17

  input = a1;
  output = a2;
  mode = a4;//mode == 1 Decrypt
  key = 0xDEADBEEF01234567;
  do
  {
    v8 = *passwordAddr;
    key = (((777 * v8 ^ 3333 * ((0x777777 * key + 12345) & 0x7FFFFFFFFFFFFFFF)) >> 13) ^ 777 * v8 ^ 3333 * ((0x777777 * key + 12345) & 0x7FFFFFFFFFFFFFFF)) + 0x5555555555555555;
    if ( v8 )
    {
      v9 = 0;
      do
      {
        key = (0x777777 * key + 12345) & 0x7FFFFFFFFFFFFFFF;
        ++v9;
      }
      while ( v9 != v8 );
    }

    v10 = 66;
    do
    {
      key = (0x777777 * key + 12345) & 0x7FFFFFFFFFFFFFFF;
      --v10;
    }
    while ( v10 );
    ++passwordAddr;//passwordAddr += 1
  }
  while ( v8 );

  v11 = 7;
  while ( 1 )
  {
    result = fgetc(input);
    v16 = result;
    if ( result == -1 )
      break;
    out = result;
    if ( v11 )
    {
      v13 = 0;
      do
      {
        key = (0x777777 * key + 12345) & 0x7FFFFFFFFFFFFFFF;
        ++v13;
      }
      while ( v11 != v13 );
    }

    if ( mode )//Decrypt
    {
      v11 = ((0x0CCCCCCCCCCCCCCCD * (21 * v11) >> 64) >> 3) ^ v16;
      out = key ^ v16;
    }

    else
    {
      out = key ^ v16;
      v11 = ((0x0CCCCCCCCCCCCCCCD * (21 * v11) >> 64) >> 3) ^ (key ^ v16);
    }
    fputc(out, output);
    fflush(output);
  }
  return result;
}
