from pathlib import path
from pyhanko.keys import load_certs_from_pemder

trust_roots = Path(__file__).parent / 'trust_roots.pem'
root_certs = list(load_certs_from_pemder([trust_roots]))

for root_cert in root_certs:
    print(root_cert.serial_number, root_cert.subject.human_friendly)
