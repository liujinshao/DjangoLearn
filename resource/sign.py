import rsa, base64

PUBLIC_KEY = b"""-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAiYKHhZUzdX/PnP3D9sJOYyDZPE2j4TZrO9Ig0av6l/yQGSbl3fNx
P5ZCk0kFjvy/zlHBj+IPhLt9cjhx18T21YjXzXYYxRX/2pL2BjOst2IpvjoY/i8a
P4RRXZuXp33T/9OvvLcrkLimRh/vg6bH3Bqbm7CstnTx2RbIVoGjTS5VGr+uQO1o
e4hZyc3A2BKugT585DwDrbqfQS4ZSpwB55zvkxPzq5FnzX/DzB95EDSmJQQXIKMU
JMeXPLsEXKa+1BINoiyCMTn4FiX2KM5IIEhyp8DWp7Yjr8ZYCtwJtykXnCspFI5K
opHYT0lBvak0z+uSGe95jmum4god7LXQswIDAQAB
-----END RSA PUBLIC KEY-----"""

PRIVATE_KEY = b"""-----BEGIN RSA PRIVATE KEY-----
MIIEqQIBAAKCAQEAiYKHhZUzdX/PnP3D9sJOYyDZPE2j4TZrO9Ig0av6l/yQGSbl
3fNxP5ZCk0kFjvy/zlHBj+IPhLt9cjhx18T21YjXzXYYxRX/2pL2BjOst2IpvjoY
/i8aP4RRXZuXp33T/9OvvLcrkLimRh/vg6bH3Bqbm7CstnTx2RbIVoGjTS5VGr+u
QO1oe4hZyc3A2BKugT585DwDrbqfQS4ZSpwB55zvkxPzq5FnzX/DzB95EDSmJQQX
IKMUJMeXPLsEXKa+1BINoiyCMTn4FiX2KM5IIEhyp8DWp7Yjr8ZYCtwJtykXnCsp
FI5KopHYT0lBvak0z+uSGe95jmum4god7LXQswIDAQABAoIBAAp8n+U6GbCOTMEG
QVmiO+QnbynAKg1U3xyyy7nxyaypoDuq0cD5fduBlBYzbW8YK3CKn55feRuASPLb
ByOTa9ehFgQfS4hMQzTiHE0gx708iT5uo9VOtku9xY7D/O7TE8Xg2PglZ/cjfdq/
OL7rizZn+RIIiUNo67BkUR5sXYJIY3dfzZystOG8s6eZfBU0OIJfnILCe3vwQMmQ
Ob97wlqPUAkk9T4kg63slrBc3cLf8ygqPYgKB2UWSTFbClVdAxAX0JJOeooHKcdv
fZescm0Q2XtNUeqTkfrnJkIqBNQhU7aNiNLSICoGH50YSG2I5Hboyl7SdcufPXgK
YYasMRECgYkA1u/7hT7zyXJ38lJtlsGwRLkQadydg65/YskRIZdKq9xF9NlNB+JR
06Z8h7ZdFuZ3yPnsAXveiCfD1fPIRrP4FPin7/x0sKnLZZML8gQKbavMIKsy25J3
tZuqHsc11lE2VEWYv1R4ylbImk/R6MgFFgFX6TokE9qBflYX5HjsUHLOE2sW8Uxf
FwJ5AKPHxYFJ6iT+Hytpy4FD/4afRlZ443sAlIsPjQFE4P+qVdjkI2Aw7ZWJ5XpZ
l+HSP0E+m4JxvQbdqFSP3rcFuJwC2XK4R+eaQBi6Y/PueTgHjt7UvYg7e08W+mrK
MarelpbE3ojxUNIu+aAQ0SF+fIKtNEAWMRr8xQKBiBfHAJoi9rEoWqCSAdGVp7xS
hMBRSZORsEHrYFvI8tfETHDjwSPII6k4V7pjsDSiVkoDa9pWK64ASCfZCiTYL++R
+nIQCZCpl/iqpb2mOMkdIj3S8pNbxqZujAlPnGMTJOF5uYYhACPSKer4PY504isn
BuSkK+2OVJj3STlbLzlPGgEH7cfP3Q0CeFBI13p/PzYPFDx1yfp92L6nSRWOgQSE
zkw0vUxH9XuehiKiAu1eTrilNkZ5sMhUBgn3pMeW9bBt69w4Alb5iPuBMhLYXvcb
WBxHEkQ7PFTI77Iv2xDzB4lHnE3I+/vkzTDvJJ9Am/vMZzWdyMaAeIyeVySrPDsc
eQKBiQCa7m1/QxliRs9W+/sqzpdCtyHGZEQalEs+KCizOewOeX3Y1UIvpw5JNf/r
JxPqKd7A9jO26+O1dAW6XVtek7bh7ojv1L5RGhID7zuPuizIvXLJJofoegBzEEQV
FFcLBcBDU96zQvaT4DlhYRt0WoKbAmS8uSfmZzPpi3TDqR9TPrk71rQZvJIb
-----END RSA PRIVATE KEY-----"""

public_key = rsa.PublicKey.load_pkcs1(PUBLIC_KEY)

private_key = rsa.PrivateKey.load_pkcs1(PRIVATE_KEY)


def sign(message):
    cyptx_text = rsa.sign(message.encode(), private_key, "SHA-1")
    return base64.b64encode(cyptx_text).decode()


def verify(message, sign_text: str):
    sign_text = sign_text.replace(" ", "+")
    cyptx_text = base64.b64decode(sign_text.encode())

    try:
        hasher = rsa.verify(message.encode(), cyptx_text, public_key)
        return hasher == "SHA-1"

    except BaseException as e:
        return False