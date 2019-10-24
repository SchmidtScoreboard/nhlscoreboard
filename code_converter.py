import re


def alphabet():
    out = []
    for c in range(ord("A"), ord("Z") + 1):
        out.append(chr(c))
    return out


def ip_to_code(ip_address):
    out = ""
    alph = alphabet()
    octets = [int(x) for x in ip_address.split(".")]
    for octet in octets:
        mod = octet // len(alph)
        rem = octet % len(alph)
        out += "{}{}".format(alph[mod], alph[rem])
    return out


def code_to_ip(code):
    pairs = re.findall('..', code)
    alph = alphabet()
    out = ""
    for pair in pairs:
        mod = alph.index(pair[0])
        rem = alph.index(pair[1])
        out += ("{}.".format(mod * len(alph) + rem))
    return out.rstrip(".")


if(__name__ == "__main__"):
    print(ip_to_code("10.255.260.10"))
    print(code_to_ip("AKJVKAAK"))
