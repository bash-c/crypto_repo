#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__Auther__ = 'M4x'

import base64
import codecs
from Crypto.Cipher import AES

c = AES.new(b'Hello, World...!')
print(codecs.encode(c.decrypt(b"Good Plain Text!"), "hex_codec"))
