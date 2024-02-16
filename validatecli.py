import argparse
import io

from pdftitle import get_title_from_io
from pyhanko.keys import load_certs_from_pemder
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_ltv_signature, RevocationInfoValidationType

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input PDF file to be validated.", type=str)

args = parser.parse_args()

root_certs = list(load_certs_from_pemder(['trust_roots.pem']))


with open(args.input_file, 'rb') as f:
    data = io.BytesIO(f.read())
    print('Title: ' + get_title_from_io(data))

    data.seek(0)
    r = PdfFileReader(data)

    for sig in r.embedded_signatures:
        cert_subj = sig.signer_cert[0]["subject"]

        sig_status = validate_pdf_ltv_signature(
            sig,
            validation_type=RevocationInfoValidationType.ADOBE_STYLE,
            validation_context_kwargs={'trust_roots': root_certs}
        )

        signer_text = cert_subj.native['serial_number'] + ' ' + cert_subj.native['common_name']

        if not sig_status.bottom_line:
            raise RuntimeError('Failed to validate signature for: ' + signer_text)

        print('OK ' + signer_text + ' ' + sig_status.timestamp_validity.timestamp.isoformat())
