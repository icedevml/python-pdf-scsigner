import argparse
import getpass
import io
import os

from pkcs11 import PKCS11Error

from libhanko import check_token_present, sign_pdf

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input PDF file to be signed.", type=str)
parser.add_argument("--output_file", help="Output PDF file to be signed.", type=str)

args = parser.parse_args()

try:
    check_token_present()
except PKCS11Error as e:
    print('PKCS11Error: ' + str(e))

with open(args.input_file, 'rb') as f:
    input_data = io.BytesIO(f.read())

print('Creating PIN entry prompt...')
user_pin = getpass.getpass('PIN: ')
output_data = sign_pdf(input_data, user_pin)

if args.output_file:
    output_file = args.output_file
else:
    file_name = os.path.basename(args.input_file)
    file_dir = os.path.dirname(args.input_file)
    output_file = os.path.join(file_dir, 'signed-' + file_name)

with open(output_file, 'wb') as f:
    f.write(output_data)
