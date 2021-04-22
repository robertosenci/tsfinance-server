#!/usr/bin/env python
# coding: utf-8

import json
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


def encript(data, key, iv):
    """ o tamanho do key é 32"""
    """ o tamanho do iv é 16"""

    data = json.dumps(data).encode()
    key = key.replace('.', '')
    key = bytes(key, 'utf-8')

    iv = iv.replace('.', '').replace('-', '')
    iv = bytes(iv, 'utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    ct = b64encode(ct_bytes).decode('utf-8')
    return ct


def decript(dado, server, key):
    key = key.replace('.', '')
    key = bytes(key, 'utf-8')
    iv = server.replace('.', '').replace('-', '')
    iv = bytes(iv, 'utf-8')
    ct = b64decode(dado)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return json.loads(pt.decode('utf-8'))


