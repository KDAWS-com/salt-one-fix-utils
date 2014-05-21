
# -*- coding: utf-8 -*-
'''
Use pycrypto to generate random passwords on the fly.
'''

# Import python libraries
try:
    import Crypto.Random  # pylint: disable=E0611
    HAS_RANDOM = True
except ImportError:
    HAS_RANDOM = False
import crypt
import re
import string
import random

# Import salt libs
import salt.exceptions

def secure_password(length=20):
    '''
    Generate a secure password.
    '''
    pw = ''
    while len(pw) < length:
        if HAS_RANDOM:
            pw += re.sub(r'\W', '', Crypto.Random.get_random_bytes(1))
        else:
            pw += random.choice(string.ascii_letters + string.digits)
    return pw


def gen_hash(crypt_salt=None, password=None, algorithm='sha512'):
    '''
    Generate /etc/shadow hash
    '''
    hash_algorithms = {'md5':'$1$', 'blowfish':'$2a$', 'sha256':'$5$', 'sha512':'$6$'}
    if algorithm not in hash_algorithms:
        raise salt.exceptions.SaltInvocationError('Not support {0} algorithm'.format(algorithm))

    if password is None:
        password = secure_password()

    if crypt_salt is None:
        crypt_salt = secure_password(8)

    crypt_salt = hash_algorithms[algorithm] + crypt_salt

    return crypt.crypt(password, crypt_salt)
