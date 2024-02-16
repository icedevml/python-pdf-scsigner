import random
import string
from io import BytesIO

from pkcs11 import ObjectClass, Attribute
from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.pkcs11 import PKCS11Signer, open_pkcs11_session
from pyhanko_certvalidator import ValidationContext
from pyhanko_certvalidator.fetchers.requests_fetchers import RequestsFetcherBackend

from config import PKCS11_LIB, PKCS11_TOKEN_LABEL


def _open_session(user_pin=None):
    return open_pkcs11_session(
        lib_location=PKCS11_LIB,
        token_label=PKCS11_TOKEN_LABEL,
        user_pin=user_pin
    )


def check_token_present():
    pkcs11_session = _open_session()
    pkcs11_session.close()


def sign_pdf(input_data: BytesIO, user_pin: str):
    pkcs11_session = _open_session(user_pin)

    objs = list(pkcs11_session.get_objects({Attribute.CLASS: ObjectClass.CERTIFICATE}))
    obj_id = objs[0][Attribute.ID]

    cms_signer = PKCS11Signer(
        pkcs11_session=pkcs11_session,
        cert_id=obj_id,
        key_id=obj_id)

    validation_context = ValidationContext(
        fetcher_backend=RequestsFetcherBackend(),
        allow_fetching=True
    )

    random_val = ''.join(random.choice(string.digits) for _ in range(12))
    out = signers.sign_pdf(
        IncrementalPdfFileWriter(input_data),
        signers.PdfSignatureMetadata(
            field_name='Signature' + random_val,
            validation_context=validation_context,
            embed_validation_info=True),
        signer=cms_signer
    )

    return out.read()
