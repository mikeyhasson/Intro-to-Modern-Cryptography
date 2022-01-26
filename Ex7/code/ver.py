import sys
import hashlib

Nb = 256
NB = Nb//8 
ONE_TIME_SIG_LEN = NB*Nb 
VK_LEN = NB*Nb*2 
SIG_LEN = (2*VK_LEN + ONE_TIME_SIG_LEN) * Nb 

def str_pop(l,n):
    return l[:n],l[n:]

def bits(x):
    bits = []
    for y in x:
        for i in range(8):
            y, b = divmod(y,2)
            bits.append(b)
    return bits
            
def SHA(x):
    return hashlib.sha256(x).digest()

def init_vk(vk_bytes):
    vk = []
    while vk_bytes:
        k0, vk_bytes = str_pop(vk_bytes, NB)
        k1, vk_bytes = str_pop(vk_bytes, NB)
        vk.append((k0, k1))
    return vk

def one_time_ver(vk, msg, sig):
    msg = SHA(msg)
    for b, keys in zip(bits(msg), vk):
        key, sig = str_pop(sig, NB)
        if keys[b] != SHA(key):
            return False
    return True

def ver(vk, msg, sig):
    if len(sig) != SIG_LEN:
        return False
    msg = SHA(msg)
    for b in bits(msg):
        vk0_bytes, sig = str_pop(sig, VK_LEN)
        vk1_bytes, sig = str_pop(sig, VK_LEN)
        vk_sig, sig = str_pop(sig, ONE_TIME_SIG_LEN)
        if not one_time_ver(vk, vk0_bytes + vk1_bytes, vk_sig):
            return False
        vk = init_vk((vk0_bytes, vk1_bytes)[b])
    return True
    
def main():
    try:
        (msg, vk_file, sig_file) = sys.argv[1:]
    except ValueError:
        print("Usage: ver.py message key_file signature_file")
        return

    vk = init_vk(open(vk_file,'rb').read())
    sig = open(sig_file,'rb').read()
    print(ver(vk, msg.encode(), sig))

main()
