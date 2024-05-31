import hashlib
import sys
from Crypto.Cipher import AES

def gen_key(id):
	h = hashlib.md5(id.encode()).digest()
	key = h[0:1] + h[-1:] + h[-1:1:-1]
	print(f"Unrotated key \t: {key.hex()}")
	return key 

def rrotate(key, n):
	rotated = b""
	print(f"Rotation\t: {n}")
	for i in range(len(key)):
		off = (i + n) % len(key)
		rotated += key[off:off+1]
	return rotated

if __name__ == "__main__" :
	if len(sys.argv) != 3 :
		print("Usage : py acsavedit.py <file_path> <id>")
		exit(1)
	with open(sys.argv[1], "rb") as f :
		print(f"ID used\t: {sys.argv[2]}")
		data	= f.read()
		ct_data = data[0x228:]
		key		= rrotate(gen_key(sys.argv[2]), len(ct_data) % 16 - 1)
		print(f"Rotated key\t: {key.hex()}")
		print(f"Data length\t: {len(ct_data)}")
		with open(sys.argv[1] + ".hkd", "wb") as out :
			i = 0
			out.write(data[:0x228])
			for b in ct_data :
				out.write(bytes([b ^ key[i % 16]]))
				i += 1