from hashlib import sha256
from itertools import permutations
import binascii

# The tree’s root encoded in hex is:
hash_last_line = "40c239bf3880461563d09da5078cc28cbef4917c51afb2e21ca1e42dc89c3fa2"
f = open("/Users/mikeyhasson/programing/crypto/ex3/solution/code/students.txt", "r")
students = [line.strip() for line in f.readlines()]
f.close()
NAME = "Michael Hasson"

def calc_hash_name(name):
    return sha256(bytes(name,'ascii')).digest()

def calc_hash_bytes(bytes_arg):
    return sha256(bytes_arg).digest()

def compute_root (name):
    # For each line in the file, read the name, transform it into a sequence of bytes using ASCII encoding,
    # hash the bytes and write back the hash.
    students_hash = [calc_hash_name(student) for student in students]
    my_index = students.index(name)
    # (2)For each pair of lines in the file, read the two hash values and concatenate them.
    # Hash the resulting 512 bits and write back the hash
    # Repeat step (2) until there is only one line left in the file, containing the root

    while len(students_hash) != 1:
        temp_hash=[]
        for k,i in enumerate(range(0, len(students_hash), 2)):
            val=calc_hash_bytes(students_hash[i]+students_hash[i+1])
            if i==my_index or i+1 ==my_index:
                my_index = k
                print(students_hash[i].hex()+students_hash[i+1].hex())
            temp_hash.append(val)
        students_hash=temp_hash

    root_bytes = students_hash[0]
    print("root:",root_bytes.hex())


if __name__ == "__main__":
    root = compute_root("Michael Hasson")


