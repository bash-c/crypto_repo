### 0x01 ffa

这个题就只想说z3大法好了。

```python
#!/usr/bin/env python3
import sympy
import json

m = sympy.randprime(2**257, 2**258)
M = sympy.randprime(2**257, 2**258)
a, b, c = [(sympy.randprime(2**256, 2**257) % m) for _ in range(3)]

x = (a + b * 3) % m
y = (b - c * 5) % m
z = (a + c * 8) % m

flag = int(open('flag', 'rb').read().strip().hex(), 16)
p = pow(flag, a, M)
q = pow(flag, b, M)

json.dump({ key: globals()[key] for key in "Mmxyzpq" }, open('crypted', 'w'))
# {"p": 240670121804208978394996710730839069728700956824706945984819015371493837551238, "q": 63385828825643452682833619835670889340533854879683013984056508942989973395315, "M": 349579051431173103963525574908108980776346966102045838681986112083541754544269, "z": 213932962252915797768584248464896200082707350140827098890648372492180142394587, "m": 282832747915637398142431587525135167098126503327259369230840635687863475396299, "x": 254732859357467931957861825273244795556693016657393159194417526480484204095858, "y": 261877836792399836452074575192123520294695871579540257591169122727176542734080}
```

程序的逻辑很简单，生成了几个大随机数**M, m, x, y, z, p, q**，通过分析代码不难得出如果得到a或者b就能得到flag，但问题就在于，怎么求出a或者b。

刚开始的想法是通过有限域的方法化简，得到a或者b，但正要动手时转念一想，题上的约束关系都很明确，可以用z3试一下，于是写了z3求解的代码：

```python
def getabc():
    a = BitVec("a", 265)
    b = BitVec("b", 265)
    c = BitVec("c", 265)
    x = d["x"]
    y = d["y"]
    z = d["z"]
    m = d["m"]
    #  print x, y, z
    s = Solver()
    s.add(UGT(a, pow(2, 256, m)))
    s.add(ULT(a, pow(2, 257, m)))
    s.add(UGT(b, pow(2, 256, m)))
    s.add(ULT(b, pow(2, 257, m)))
    s.add(UGT(c, pow(2, 256, m)))
    s.add(ULT(c, pow(2, 257, m)))
    s.add(x == (a + b * 3) % m)
    s.add(y == (b - c * 5) % m)
    s.add(z == (a + c * 8) % m)
    
    while s.check() == sat:
        if isPrime(s.model()[a].as_long()) and isPrime(s.model()[b].as_long()) and isPrime(s.model()[c].as_long()):
            print s.model()
        A, B, C = s.model()[a].as_long(), s.model()[b].as_long(), s.model()[c].as_long()
        s.add(Or(a != s.model()[a], b != s.model()[b], c != s.model()[c]))
    else:
        print "Finished"
        return A, B, C
```

> 有两点需要注意：
>
> 1. 用BitVec声明变量时，首先要估算中间变量的范围，确保运算过程中数据不会溢出(如该题中使用了较大的265位)，但为了运行速度也不能过大
> 2. 大整数的比较大小建议使用UGT/ULT代替>/<

本来运行的时候还替z3担心了一下会不会因为数据太大直接崩掉，但没想到用了短短的8s就跑出了结果

![](https://ws1.sinaimg.cn/large/006AWYXBly1fntrjndsyyj30k507gdjy.jpg)

计算出a，b，c后，主要问题就解决了。

意识到使用flag的加密实际上是RSA时，利用a和b进行了共模攻击，很快就出flag了

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__Auther__ = 'M4x'

from libnum import prime_test as isPrime
from libnum import n2s, xgcd, invmod
from z3 import *

d = {"p": 240670121804208978394996710730839069728700956824706945984819015371493837551238, "q": 63385828825643452682833619835670889340533854879683013984056508942989973395315, "M": 349579051431173103963525574908108980776346966102045838681986112083541754544269, "z": 213932962252915797768584248464896200082707350140827098890648372492180142394587, "m": 282832747915637398142431587525135167098126503327259369230840635687863475396299, "x": 254732859357467931957861825273244795556693016657393159194417526480484204095858, "y": 261877836792399836452074575192123520294695871579540257591169122727176542734080}

def getabc():
    a = BitVec("a", 265)
    b = BitVec("b", 265)
    c = BitVec("c", 265)
    x = d["x"]
    y = d["y"]
    z = d["z"]
    m = d["m"]
    #  print x, y, z
    s = Solver()
    s.add(UGT(a, pow(2, 256, m)))
    s.add(ULT(a, pow(2, 257, m)))
    s.add(UGT(b, pow(2, 256, m)))
    s.add(ULT(b, pow(2, 257, m)))
    s.add(UGT(c, pow(2, 256, m)))
    s.add(ULT(c, pow(2, 257, m)))
    s.add(x == (a + b * 3) % m)
    s.add(y == (b - c * 5) % m)
    s.add(z == (a + c * 8) % m)
    
    while s.check() == sat:
        if isPrime(s.model()[a].as_long()) and isPrime(s.model()[b].as_long()) and isPrime(s.model()[c].as_long()):
            print s.model()
        A, B, C = s.model()[a].as_long(), s.model()[b].as_long(), s.model()[c].as_long()
        s.add(Or(a != s.model()[a], b != s.model()[b], c != s.model()[c]))
    else:
        print "Finished"
        return A, B, C

def getFlag((a, b, c)):
    M = d["M"]
    p = d["p"]
    q = d["q"]
    s1, s2, _ = xgcd(a, b)
    if s1 < 0:
        s1 = -s1
        p = invmod(p, M)
    elif s2 < 0:
        s2 = -s2
        q = invmod(q, M)

    flag = (pow(p, s1, M) * pow(q, s2, M)) % M
    print n2s(flag)
    

if __name__ == "__main__":
    #  getabc()
    getFlag(getabc())
```

整个脚本也才8s左右

![](https://ws1.sinaimg.cn/large/006AWYXBly1fntrmcv0rtj30t705378b.jpg)

> OwO多了一步求flag的过程，计算时间反而更短了，看来计算时间还是跟CPU的心情有关系