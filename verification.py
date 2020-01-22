from random import randint
import binascii
p = 531872289054204184185084734375133399408303613982130856645299464930952178606045848877129147820387996428175564228204785846141207532462936339834139412401975338705794646595487324365194792822189473092273993580587964571659678084484152603881094176995594813302284232006001752128168901293560051833646881436219
g = 5
DIGITS = 300


def generate():
    range_start = 10**(DIGITS-1)
    range_end = (10**DIGITS)-1
    return randint(range_start, range_end)


# return the message as a hex string
# message is just a string
def encrypt(shared_secret, message):
    hex_message = binascii.hexlify(message)
    message_int = int(hex_message, 16)
    return hex(message * shared_secret)


# given an encrypted hex string, give the decoded message
def decrypt(shared_secret, encrypted_message_hex):
    encrypted_int = int(encrypted_message_hex, 16)
    decrypted_int = encrypted_int / shared_secret
    return binascii.unhexlify(hex(decrypted_int))


def getPublicKey(private_key):
    return pow(g, private_key, p)


def getSharedSecret(their_public_key, my_private_key):
    return pow(their_public_key, my_private_key,  p)


if __name__ == "__main__":
    alicePrivateKey = generate()
    bobPrivateKey = generate()

    alicePublicKey = getPublicKey(alicePrivateKey)
    bobPublicKey = getPublicKey(bobPrivateKey)

    aliceSecret = getSharedSecret(bobPublicKey, alicePrivateKey)
    bobSecret = getSharedSecret(alicePublicKey, bobPrivateKey)

    if aliceSecret != bobSecret:
        print("Secret exchange failed\n{}\n{}".format(aliceSecret, bobSecret))
    else:
        print("Secret exchange succeeded")

    text = "hello world"
    encrypted_text = encrypt(aliceSecret, text)
    decrypted_text = decrypt(bobSecret, encrypted_text)

    if(decrypted_text != text):
        print("Encryption failed\n{}\n{}".format(decrypted_text, text))
    else:
        print("Encryption succeeded")
