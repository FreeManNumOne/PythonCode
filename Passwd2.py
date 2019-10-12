#coding: utf8
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
 
class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
 
if __name__ == '__main__':
    pc = prpcrypt('xxxxxxx')
    d = pc.decrypt('625787c88d24455833a44d07a47cc12b8d041a8d2b5bc1328431be020e7e456e')                  
    print d
