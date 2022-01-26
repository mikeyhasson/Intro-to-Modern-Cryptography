from ver import *
import secrets

def init_sk(sk_bytes):
    return init_vk(sk_bytes)

def keygen():
    sk = [[0 for x in range(2)] for y in range(256)]
    pk = [[0 for x in range(2)] for y in range(256)]
    for i in range(0,256):
        #secret key
        sk[i][0] = secrets.token_bytes(32)
        sk[i][1] = secrets.token_bytes(32)
        #public key
        pk[i][0] = SHA(sk[i][0])
        pk[i][1] = SHA(sk[i][1])

    keypair = [sk,pk]
    return keypair

def one_time_ver_crack(vk, msg, sig,sk):
    msg = SHA(msg)
    for b, keys,keys_sk,sig_i in zip(bits(msg), vk,sk,sig):
        key, sig = str_pop(sig, NB)
        if keys_sk[b] != None and keys_sk[b]!=key:
            print("aaa")

        keys_sk[b]=key
        if keys[b] != SHA(key):
            return False
    return True

def one_time_sig(sk, msg):
    msg = SHA(msg)
    return [keys[b] for b, keys in zip(bits(msg), sk)]

def bits_to_str(b):
    return "".join([str(x) for x in b])

def signature_fake (sec_key,val_key,msg):
    msg = SHA(msg)
    msg_bits = bits(msg)
    used_keys= []
    i=0
    d={}
    out = b''
    d['']= (sec_key,val_key)
    used_keys.append(sec_key)
    for i in range(len(msg_bits)):
        one_time_arr = [None]
        while None in one_time_arr:
            x = bits_to_str(msg_bits[:i])
            (sk, vk) = d[x]

            for b in [0,1]:
                keys = keygen()
                while keys[0] in used_keys:
                    keys=keygen()

                sk_b = keys[0]
                vk_b = keys[1]
                d[x + str(b)] = (sk_b,vk_b)

            vk_0 =d[x +'0'][1]
            vk_1 =d[x +'1'][1]

            vk_str = b''.join([b''.join([(vk_i[0]+vk_i[1]) for vk_i in vk]) for vk in [vk_0,vk_1]])
            one_time_arr = one_time_sig(sk, vk_str)
        one_time_sig_bytes = b"".join(one_time_arr)

        out +=vk_str +one_time_sig_bytes

    return out
def signature (sec_key,val_key,msg):
    msg = SHA(msg)
    msg_bits = bits(msg)
    used_keys= []
    i=0
    d={}
    out = b''
    d['']= (sec_key,val_key)
    used_keys.append(sec_key)
    for i in range(len(msg_bits)):
        x = bits_to_str(msg_bits[:i])
        (sk, vk) = d[x]

        for b in [0,1]:
            keys = keygen()
            while keys[0] in used_keys:
                keys=keygen()

            sk_b = keys[0]
            used_keys.append(sk_b)
            vk_b = keys[1]
            d[x + str(b)] = (sk_b,vk_b)

        vk_0 =d[x +'0'][1]
        vk_1 =d[x +'1'][1]

        vk_str = b''.join([b''.join([(vk_i[0]+vk_i[1]) for vk_i in vk]) for vk in [vk_0,vk_1]])
        one_time_sig_bytes = b"".join([x for x in one_time_sig(sk,vk_str)])

        out +=vk_str +one_time_sig_bytes


def flaw_to_sign_id(id):
    x='a'
    sk = [[None for x in range(2)] for y in range(256)]
    keys = []

    while x != 'f':
        vk = init_vk(open("vk2", 'rb').read())
        msg = x.encode()
        msg = SHA(msg)
        sig = open(str(x)+".sig",'rb').read()
        for b in bits(msg)[:1]:
            vk0_bytes, sig = str_pop(sig, VK_LEN)
            vk1_bytes, sig = str_pop(sig, VK_LEN)
            vk_sig, sig = str_pop(sig, ONE_TIME_SIG_LEN)
            sum_vk=vk0_bytes + vk1_bytes
            if not one_time_ver_crack (vk, sum_vk, vk_sig,sk):
                return False

            vk = init_vk((vk0_bytes, vk1_bytes)[b])
            keys.append(vk)
        x= chr(ord(x)+1)

    sig = signature_fake(sk,init_vk(open("vk2", 'rb').read()),id.encode())
    print(ver(init_vk(open("vk2", 'rb').read()),id.encode(),sig))
    open(id+"sig",'wb').write(sig)
    return True


def main():
    '''try:
        (msg,sk_file, vk_file) = sys.argv[1:]
    except ValueError:
        print("Usage: sig.py message signing_key_file verification_key_file")
        return'''

    '''for msg in ['Michael','Hasson']:
        vk_file = "vk1"
        sk_file = "sk1"
        vk = init_vk(open(vk_file, 'rb').read())
        sk = init_sk(open(sk_file, 'rb').read())
        sign = signature(sk,vk,msg.encode())
        open(msg + ".sig", 'wb').write(sign)
        assert(ver(vk, msg.encode(), sign))'''


    vk_file = "vk2"
    msg="a"
    sign = open('a.sig','rb').read()
    print(flaw_to_sign_id("322893892"))


main()