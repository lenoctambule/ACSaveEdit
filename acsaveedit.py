import hashlib
import sys
import deflate

def gen_key(id):
	h = hashlib.md5(id.encode()).digest()
	key = h[0:1] + h[-1:] + h[-1:1:-1]
	return key 

def rrotate(key, n):
	rotated = b""
	for i in range(len(key)):
		off = (i + n) % len(key)
		rotated += key[off:off+1]
	return rotated

if __name__ == "__main__" :
	if len(sys.argv) != 4 :
		print("Usage : py acsavedit.py <file_path> <id> <new_id>")
		exit(1)
	with open(sys.argv[1], "rb") as f :
		data	= f.read()
		ct_data = data[0x228:]
		key		= rrotate(gen_key(sys.argv[2]), len(ct_data) % 16 - 1)
		new_key = rrotate(gen_key(sys.argv[3]), len(ct_data) % 16 - 1)
		with open(sys.argv[1] + ".hkd", "wb") as out :
			i = 0
			new_data = b""
			new_data += data[:0x228]
			for b in ct_data :
				new_data += bytes([(b ^ key[i % 16]) ^ new_key[i % 16]])
				i += 1
			out.write(new_data)