import struct,os
from bitarray import bitarray
from math import (
    floor,
    sin,
)

import hashlib




class MD5():
    bit_add = lambda a, b: (a + b) % pow(2, 32)
    shift_left = lambda x, n: (x << n) | (x >> (32 - n))

    @classmethod
    def R(cls, func, a, b, c, d, x, s, t):
        res = cls.bit_add(func(b, c, d), x)
        res = cls.bit_add(res, t)
        res = cls.bit_add(res, a)
        res = cls.shift_left(res, s)
        res = cls.bit_add(res, b)
        return res

    @classmethod
    def generate_hash(cls, str):
        cls._A = 0x67452301
        cls._B = 0xEFCDAB89
        cls._C = 0x98BADCFE
        cls._D = 0x10325476

        b_array = cls.step_1(str)
        b_array = cls.step_2(len(str), b_array)

        cls.step_4(b_array)

        return cls._step_5()

    @classmethod
    def step_1(cls, str):
        b_array = bitarray()
        b_array.frombytes(str)

        b_array.append(1)

        while b_array.length() % 512 != 448:
            b_array.append(0)

        return bitarray(b_array)

    @classmethod
    def step_2(cls, str_len, s1_array):
        b_len = (str_len * 8) % pow(2, 64)

        b_array_len = bitarray()
        b_array_len.frombytes(struct.pack("<Q", b_len))

        res = s1_array.copy()
        res.extend(b_array_len)

        return res

    # Шаг 3 произведен в объявлении класса

    @classmethod
    def step_4(cls, b_array):
        F = lambda b, c, d: (b & c) | (~b & d)
        G = lambda b, c, d: (b & d) | (c & ~d)
        H = lambda b, c, d: b ^ c ^ d
        I = lambda b, c, d: c ^ (b | ~d)

        T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]

        N = len(b_array) // 32

        for block_idx in range(0, N // 16, 512):
            a, b, c, d = cls._A, cls._B, cls._C, cls._D

            X = [b_array[block_idx + (x * 32): block_idx + (x * 32) + 32] for x in range(16)]

            X = [int.from_bytes(word.tobytes(), byteorder="little") for word in X]

            s1 = [7, 12, 17, 22]
            s2 = [5, 9, 14, 20]
            s3 = [4, 11, 16, 23]
            s4 = [6, 10, 15, 21]

            # Раунд 2
            a = cls.R(F, a, b, c, d, X[0], s1[0], T[0])
            d = cls.R(F, d, a, b, c, X[1], s1[1], T[1])
            c = cls.R(F, c, d, a, b, X[2], s1[2], T[2])
            b = cls.R(F, b, c, d, a, X[3], s1[3], T[3])
            a = cls.R(F, a, b, c, d, X[4], s1[0], T[4])
            d = cls.R(F, d, a, b, c, X[5], s1[1], T[5])
            c = cls.R(F, c, d, a, b, X[6], s1[2], T[6])
            b = cls.R(F, b, c, d, a, X[7], s1[3], T[7])
            a = cls.R(F, a, b, c, d, X[8], s1[0], T[8])
            d = cls.R(F, d, a, b, c, X[9], s1[1], T[9])
            c = cls.R(F, c, d, a, b, X[10], s1[2], T[10])
            b = cls.R(F, b, c, d, a, X[11], s1[3], T[11])
            a = cls.R(F, a, b, c, d, X[12], s1[0], T[12])
            d = cls.R(F, d, a, b, c, X[13], s1[1], T[13])
            c = cls.R(F, c, d, a, b, X[14], s1[2], T[14])
            b = cls.R(F, b, c, d, a, X[15], s1[3], T[15])

            # Раунд 2
            a = cls.R(G, a, b, c, d, X[1], s2[0], T[16])
            d = cls.R(G, d, a, b, c, X[6], s2[1], T[17])
            c = cls.R(G, c, d, a, b, X[11], s2[2], T[18])
            b = cls.R(G, b, c, d, a, X[0], s2[3], T[19])
            a = cls.R(G, a, b, c, d, X[5], s2[0], T[20])
            d = cls.R(G, d, a, b, c, X[10], s2[1], T[21])
            c = cls.R(G, c, d, a, b, X[15], s2[2], T[22])
            b = cls.R(G, b, c, d, a, X[4], s2[3], T[23])
            a = cls.R(G, a, b, c, d, X[9], s2[0], T[24])
            d = cls.R(G, d, a, b, c, X[14], s2[1], T[25])
            c = cls.R(G, c, d, a, b, X[3], s2[2], T[26])
            b = cls.R(G, b, c, d, a, X[8], s2[3], T[27])
            a = cls.R(G, a, b, c, d, X[13], s2[0], T[28])
            d = cls.R(G, d, a, b, c, X[2], s2[1], T[29])
            c = cls.R(G, c, d, a, b, X[7], s2[2], T[30])
            b = cls.R(G, b, c, d, a, X[12], s2[3], T[31])

            # Раунд 3
            a = cls.R(H, a, b, c, d, X[5], s3[0], T[32])
            d = cls.R(H, d, a, b, c, X[8], s3[1], T[33])
            c = cls.R(H, c, d, a, b, X[11], s3[2], T[34])
            b = cls.R(H, b, c, d, a, X[14], s3[3], T[35])
            a = cls.R(H, a, b, c, d, X[1], s3[0], T[36])
            d = cls.R(H, d, a, b, c, X[4], s3[1], T[37])
            c = cls.R(H, c, d, a, b, X[7], s3[2], T[38])
            b = cls.R(H, b, c, d, a, X[10], s3[3], T[39])
            a = cls.R(H, a, b, c, d, X[13], s3[0], T[40])
            d = cls.R(H, d, a, b, c, X[0], s3[1], T[41])
            c = cls.R(H, c, d, a, b, X[3], s3[2], T[42])
            b = cls.R(H, b, c, d, a, X[6], s3[3], T[43])
            a = cls.R(H, a, b, c, d, X[9], s3[0], T[44])
            d = cls.R(H, d, a, b, c, X[12], s3[1], T[45])
            c = cls.R(H, c, d, a, b, X[15], s3[2], T[46])
            b = cls.R(H, b, c, d, a, X[2], s3[3], T[47])

            # Раунд 4
            a = cls.R(I, a, b, c, d, X[0], s4[0], T[48])
            d = cls.R(I, d, a, b, c, X[7], s4[1], T[49])
            c = cls.R(I, c, d, a, b, X[14], s4[2], T[50])
            b = cls.R(I, b, c, d, a, X[5], s4[3], T[51])
            a = cls.R(I, a, b, c, d, X[12], s4[0], T[52])
            d = cls.R(I, d, a, b, c, X[3], s4[1], T[53])
            c = cls.R(I, c, d, a, b, X[10], s4[2], T[54])
            b = cls.R(I, b, c, d, a, X[1], s4[3], T[55])
            a = cls.R(I, a, b, c, d, X[8], s4[0], T[56])
            d = cls.R(I, d, a, b, c, X[15], s4[1], T[57])
            c = cls.R(I, c, d, a, b, X[6], s4[2], T[58])
            b = cls.R(I, b, c, d, a, X[13], s4[3], T[59])
            a = cls.R(I, a, b, c, d, X[4], s4[0], T[60])
            d = cls.R(I, d, a, b, c, X[11], s4[1], T[61])
            c = cls.R(I, c, d, a, b, X[2], s4[2], T[62])
            b = cls.R(I, b, c, d, a, X[9], s4[3], T[63])

            cls._A = (a + cls._A) & 0xffffffff
            cls._B = (b + cls._B) & 0xffffffff
            cls._C = (c + cls._C) & 0xffffffff
            cls._D = (d + cls._D) & 0xffffffff

    @classmethod
    def _step_5(cls):
        # Convert the buffers to little-endian.
        A = struct.unpack("<I", struct.pack(">I", cls._A))[0]
        B = struct.unpack("<I", struct.pack(">I", cls._B))[0]
        C = struct.unpack("<I", struct.pack(">I", cls._C))[0]
        D = struct.unpack("<I", struct.pack(">I", cls._D))[0]

        # Output the buffers in lower-case hexadecimal format.
        return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"


#print(hashlib.md5(b'Hello World').hexdigest())
#print(MD5.generate_hash(b'Hello World'))
#print(b'12345')


a = MD5.generate_hash(b'12345')
b = MD5.generate_hash(b'1345')

with open('CheckHash.txt', 'w') as checkFile:
    checkFile.write(a)
with open('CurrentHash.txt', 'w') as CurrenFile:
    CurrenFile.write(b)

print(a)
print(b)

with open('CheckHash.txt') as checkFile:
   with open('CurrentHash.txt') as CurrenFile:
      checkFileList = checkFile.read().splitlines()
      CurrenFileList = CurrenFile.read().splitlines()
      checkFileLength = len(checkFileList)
      CurrenFileLength = len(CurrenFileList)
      if checkFileLength == CurrenFileLength:
          for i in range(len(checkFileList)):
              if checkFileList[i] == CurrenFileList[i]:
                  print ( checkFileList[i] + "==" + CurrenFileList[i])
              else:                  
                  print (checkFileList[i] + " != " + CurrenFileList[i]+" Not-Equel")
      else:
          print ("ОБРАБОТКА ОШИБОК")
#os.remove('CheckHash.txt')
#os.remove('CurrentHash.txt')