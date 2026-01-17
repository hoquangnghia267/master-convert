import datetime
from typing import Any
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from ..core.base import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.exceptions import ValidationError, ConversionError
from ..core.arguments import InterfaceBuilder, ArgumentType

class CSRConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "csr"

    @property
    def help(self) -> str:
        return "Decode CSR details or Generate new CSR"

    def configure_args(self, builder: InterfaceBuilder):
        group = builder.add_group(exclusive=True, required=True)

        # Decode Mode
        group.add_argument("decode_csr", type=ArgumentType.TEXT, metavar="CSR_PEM", help="Decode CSR PEM string")

        # Generate Mode (Trigger)
        group.add_argument("generate_csr", type=ArgumentType.FLAG, action="store_true", help="Generate a new CSR")

        # Group generation options for better UI organization (still global logic-wise)
        gen_group = builder.add_group(required=False)
        gen_group.add_argument("cn", metavar="COMMON_NAME", help="Common Name (e.g. example.com)")
        gen_group.add_argument("c", metavar="COUNTRY", help="Country Code (e.g. US)")
        gen_group.add_argument("st", metavar="STATE", help="State/Province")
        gen_group.add_argument("l", metavar="LOCALITY", help="Locality/City")
        gen_group.add_argument("o", metavar="ORGANIZATION", help="Organization Name")
        gen_group.add_argument("ou", metavar="ORG_UNIT", help="Organizational Unit")


    def convert(self, **kwargs: Any):
        if kwargs.get('decode_csr'):
            self._decode_csr(kwargs['decode_csr'])
        elif kwargs.get('generate_csr'):
            self._generate_csr(kwargs)

    def _decode_csr(self, pem_data: str):
        try:
            csr = x509.load_pem_x509_csr(pem_data.encode('utf-8'))
            print("=== CSR Details ===")
            print(f"Subject: {csr.subject}")
            for attribute in csr.subject:
                print(f"  {attribute.oid._name}: {attribute.value}")

            # Extensions (SANs)
            try:
                san = csr.extensions.get_extension_for_class(x509.SubjectAlternativeName)
                print("Subject Alternative Names:")
                for name in san.value:
                    print(f"  {name}")
            except x509.ExtensionNotFound:
                print("No Subject Alternative Names found.")

        except Exception as e:
            raise ValidationError(f"Invalid CSR PEM: {e}")

    def _generate_csr(self, kwargs):
        cn = kwargs.get('cn')
        if not cn:
            raise ValidationError("Common Name (cn) is required for CSR generation.")

        c = kwargs.get('c')
        st = kwargs.get('st')
        l = kwargs.get('l')
        o = kwargs.get('o')
        ou = kwargs.get('ou')

        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        subject_attributes = [x509.NameAttribute(NameOID.COMMON_NAME, cn)]
        if c: subject_attributes.append(x509.NameAttribute(NameOID.COUNTRY_NAME, c))
        if st: subject_attributes.append(x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, st))
        if l: subject_attributes.append(x509.NameAttribute(NameOID.LOCALITY_NAME, l))
        if o: subject_attributes.append(x509.NameAttribute(NameOID.ORGANIZATION_NAME, o))
        if ou: subject_attributes.append(x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, ou))

        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name(subject_attributes)).sign(
            key, hashes.SHA256()
        )

        print("=== Private Key (Keep Secret) ===")
        print(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8'))

        print("\n=== CSR ===")
        print(csr.public_bytes(serialization.Encoding.PEM).decode('utf-8'))

ConverterRegistry.register(CSRConverter)
