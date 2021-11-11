import pyotp

hotp = pyotp.HOTP("base32secret3232")
print(hotp.verify("316439",1401))