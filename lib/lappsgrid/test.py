import codecs
import collections
import logging

from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
from galaxy.web.security import SecurityHelper

import galaxy.exceptions
from galaxy.util import (
    smart_str,
    unicodify
)

def run():
    #id_secret='cff03377815197df' # 567cc1640266789c'
    id_secret = '0123456789abcdef'
    cipher = Blowfish.new(smart_str(id_secret), mode=Blowfish.MODE_ECB)

    message = 'suderman@cs.vassar.edu'
    s = smart_str(message)
    # Pad to a multiple of 8 with leading "!"
    s = (b"!" * (8 - len(s) % 8)) + s
    print "S: " + s
    # Encrypt
    encrypted = cipher.encrypt(s)
    print "Encrypted: " + encrypted
    encoded = codecs.encode(encrypted, "hex")
    print "Encoded: " + encoded
    #print unicodify(codecs.encode(cipher.encrypt(s), 'hex'))
    print unicodify(encoded)

    security = SecurityHelper(id_secret=id_secret)
    print security.encode_guid(message)

if __name__ == '__main__':
    run()