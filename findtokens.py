from pkcs11 import lib as p11_lib, PKCS11Error

from config import PKCS11_LIB

lib = p11_lib(PKCS11_LIB)
slots = lib.get_slots()

for slot in slots:
    print('--')
    try:
        token = slot.get_token()
        print('Slot:')
        print(slot)
        print()
        print('Token:')
        print(token)
    except PKCS11Error as e:
        print('Slot:')
        print(slot)
        print()
        print('Token:')
        print('PKCS11Error: ' + repr(e))
