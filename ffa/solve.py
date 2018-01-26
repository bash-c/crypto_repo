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
