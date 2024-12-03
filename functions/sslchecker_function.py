import ssl
import socket
import datetime
import requests
import http.client

from OpenSSL import crypto


# get certificate in binary format
def get_cert(host, port):
    context = ssl.create_default_context()  # creates default context
    context.check_hostname = False  # set check_hostname to False
    context.verify_mode = ssl.CERT_NONE  # set mode to ssl.CERT_NONE

    try:
        conn = http.client.HTTPSConnection(host, port, context=context)
        conn.connect()  # Establish the connection

        # Get the socket used by the connection
        sock = conn.sock

        # Retrieve the peer certificate in binary DER format
        cert_binary = sock.getpeercert(binary_form=True)

        conn.close()  # Close the connection
        return cert_binary
    except Exception as e:
        print(e)
        return False


# parse certificate to user readable format
def parse_cert(cert_binary):
    # crypto.X509.
    # Convert the binary certificate to an X509 object for parsing
    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_binary)
    return x509


# Convert ASN1 date (YYYYMMDDHHMMSSZ) to dd-mm-yyyy format.
def format_date(asn1_date):
    date = datetime.datetime.strptime(asn1_date.decode("ascii"), "%Y%m%d%H%M%SZ")
    # replace the timezone to match the date
    return date.replace(tzinfo=datetime.timezone.utc)


# function to calculate how many days until the certificate expires
def days_until_expiration(cert):
    # get expiry date from certificate
    expiry_date = format_date(cert.get_notAfter())
    # get todays date as utc timezone
    today = datetime.datetime.now(datetime.timezone.utc)
    days_left = (expiry_date - today).days  # get days left for certificate to expiry
    return days_left  # return days left


# Check if the site forces HTTPS by making an HTTP request and checking for redirection.
def is_forcing_https(host):

    try:
        http_url = f"http://{host}"
        # call the hosted url with disable redirects
        response = requests.get(http_url, allow_redirects=False)
        # if status code is 301 or 302, (permanant redirect or temp. redirect) and https in headers available ->Forcing https redirect
        if response.status_code in [301, 302] and "https" in response.headers.get(
            "Location", ""
        ):
            return True
        return False  # -> Not Forcing https

    # if any error occured including site down or any other exception
    except Exception as e:
        print(f"Error checking HTTP redirection: {e}")
        return False


# Check if the TLS version is outdated
def is_tls_version_outdated(tls_version):
    outdated_versions = ["SSLv2", "SSLv3", "TLSv1", "TLSv1.1"]
    return tls_version in outdated_versions


# Extract detailed information from the certificate, including only the 'subjectAltName' extension
def get_cert_info(cert: crypto.X509, host):
    if not cert:
        return {}

    # create a cert_info empty variable
    cert_info = {}

    # Subject details
    cert_subject = cert.get_subject()  # get subject details object from certificate
    cert_info["subject"] = {
        "common_name": cert_subject.CN,
        "organization": cert_subject.O,
        "organizational_unit": getattr(cert_subject, "OU", "N/A"),
        "country": getattr(cert_subject, "C", "N/A"),
        "state": getattr(cert_subject, "ST", "N/A"),
        "locality": getattr(cert_subject, "L", "N/A"),
    }

    # Issuer details
    cert_issuer = cert.get_issuer()  # get issuer details object from certificate
    cert_info["issuer"] = {
        "common_name": getattr(cert_issuer, "CN", "N/A"),
        "organization": cert_issuer.O,
        "country": getattr(cert_issuer, "C", "N/A"),
    }

    # Serial number and version
    cert_info["serial_number"] = cert.get_serial_number()
    cert_info["version"] = cert.get_version()

    # Validity period (formatted in dd-mm-yyyy)
    cert_info["valid_from"] = format_date(cert.get_notBefore()).strftime("%d-%m-%Y")
    cert_info["valid_until"] = format_date(cert.get_notAfter()).strftime("%d-%m-%Y")

    # Check if the certificate is expired
    cert_info["is_expired"] = cert.has_expired()
    cert_info["certificate_valid"] = not cert.has_expired()

    # Check subjectAltName extension for host match and extract it
    subject_alt_name = None
    for i in range(cert.get_extension_count()):
        ext = cert.get_extension(i)
        ext_name = ext.get_short_name().decode("ascii")  # convert to readable format
        if ext_name == "subjectAltName":  # check for subjectAltName
            # store the subjectAltName in subject_alt_name after converting to string
            subject_alt_name = str(ext)
            break  # We only care about subjectAltName, so we break after finding it.
    # store subject_alt_name in cert_info
    cert_info["subject_alt_name"] = subject_alt_name.replace("DNS:", "").split(", ")

    # Check if the certificate is self-signed
    cert_info["self_signed"] = cert_subject.O == cert_issuer.O

    # Public key
    public_key = cert.get_pubkey()
    cert_info["public_key_type"] = public_key.type()
    cert_info["public_key_bits"] = public_key.bits()

    # Signature algorithm
    cert_info["signature_algorithm"] = cert.get_signature_algorithm().decode("ascii")

    # Days until expiration
    cert_info["days_until_expiration"] = days_until_expiration(cert)

    # return the certificate
    return cert_info


# Fetch TLS version and cipher info using SSLContext
def get_tls_info(host, port):
    context = ssl.create_default_context()  # create a default context
    context.check_hostname = False  # set Value for check_hostname
    context.verify_mode = ssl.CERT_NONE  # set Value for verify_mode

    response = {"data": None, "error": None}  # define response object

    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            protocol_version = ssock.version()  # TLS version
            cipher = ssock.cipher()  # Cipher info
            response["data"] = {"tls_version": protocol_version, "cipher": cipher}

    # check if Hostname is mismatched
    # Fetch TLS version and cipher info using SSLContext
    try:
        context = ssl.create_default_context()

        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                protocol_version = ssock.version()  # TLS version
                cipher = ssock.cipher()  # Cipher info
    except Exception as e:
        error_str = str(e)
        if error_str.find("Hostname mismatch"):
            response["error"] = "Hostname mismatch"  # add error to response object
        # undefined error is occured
        else:
            response["error"] = error_str  # add error string to response object
    return response
