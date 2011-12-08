'''
Created on 1.12.2011

@author: xaralis
'''
"""
ugly encoding guesser for czech encodings (could work for others too)
common use:
    unicode_s = encany(s)
    if unicode_s is None:
        raise UnicodeDecodeError("Coudl not decode string unicode_s")
"""
import re

sre_usualchars = re.compile(r'[\w\s\d.-_/\\,;:]*$', re.UNICODE)

def encany(s, charsets=('latin2', 'cp1250',)):
    '''encode from any charset traying to guess the right one'''
    ret = None

    guessed_charset = guess_enc(s)
    if guessed_charset:
        ret = try_charset(s, guessed_charset)

    if ret is None:
        for charset in charsets:
            ret = try_charset(s, charset)
            if ret is not None:
                break
    return ret


def try_charset(s, charset):
    '''tries decode using provided charset'''
    sde = s.decode(charset)
    if sre_usualchars.match(sde, re.UNICODE):
        ret = sde
    else:
        ret = None
    return ret


# accented zsZS in both encodings
encs_guess_chars = (
        ('cp1250', '\x9a\x8a\x9e\x8e',),
        ('latin2', '\xb9\xa9\xbE\xaE',),
        )

def guess_enc(s):
    '''tries to guess most common czech encodings'''
    for enc, guess_chars in encs_guess_chars:
        for c in guess_chars:
            if c in s:
                return enc
    return None

