# Python PDF Signer

Create an invisible digital signature on a PDF file using Python CLI script.

Supports [KIR SZAFIR Qualified Signature](https://elektronicznypodpis.pl). Should work with any PKCS#11 card
with up to few minor modifications.

## Installation

> **Note about Windows:** You need to install Build Tools for Visual Studio, which may be obtained from the
> [Download Visual Studio Tools page](https://visualstudio.microsoft.com/downloads/) -> Tools for Visual Studio
> -> Build Tools for Visual Studio 2022 -> Download

1. Clone the repository.
2. Create an virtualenv and install the requirements from the `requirements.txt`.
3. Copy `config.dist.py` to `config.py` and set the PKCS#11 library path correctly.
4. (Only required to verify documents) Copy `trust_roots.dist.pem` to `trust_roots.pem` and add the necessary
   qualified roots if needed.

## Signing

Run: `python3 signcli.py <input_file>`

This should produce a signature that is accepted by the 3rd party qualified signature validation software.

## Validating

Run: `python3 validatecli.py <input_file>`

Note that this validation script would barely validate any documents that were not signed using this tool.
