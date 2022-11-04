import RunLengthEncoding as RLE
import unittest


tests = ["ASdASDAWWWWsadcs fdssf3232", "kndsgsn999iisdjfnalnnnnsdf;ewowonnnse  s.gvsnrksrjjjjs", "njksgobujI(((((32rkjb 3kjk2 22))A)asss ve, me nar","AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"]

for test in tests:
    print(f"{test}")
    encoded = (RLE.encode(test))
    decoded = RLE.decode(encoded)
    if decoded == test :
        print("Passed\n")
    else :
        print("Fail")
        print(encoded)
        print(decoded)
        print()