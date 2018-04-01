#coding=utf-8
import os,sys,hashlib
from os.path import join,getsize

picked_size = 1024000

if len(sys.argv) < 2:
	print('USAGE: python dedup.py {directory} {anystringtojustprint}')
	sys.exit(-1)

def mark_gabage(l, file, seed):
	l.append(file)
	if seed == None:
		print('empty-file-gabage found: %s'%file)
	else:
		print('same as %s, gabage found: %s'%(seed,file))

hash_repo = {}
gabage = []
for root, dirs, files in os.walk(sys.argv[1]):
	if len(files) > 0:
		for file in files:
			full_path = join(root,file)
			file_size = getsize(full_path)
			if file_size <= 0:
				mark_gabage(gabage, full_path, None)
				continue
			f = open(full_path,'rb')
			bytesfromfile = f.read(picked_size)
			f.close()
			current_md5 = hashlib.md5()
			current_md5.update(bytesfromfile)
			current_md5.update(('%s'%file_size).encode('UTF-8'))
			current_md5_hex = current_md5.hexdigest()
			if current_md5_hex in hash_repo.keys():
				mark_gabage(gabage, full_path, hash_repo[current_md5_hex])
			else:
				hash_repo[current_md5_hex] = full_path
				print('keep %s'%full_path)

print("gabage summary")
print("gabage entry amount: %s"%len(gabage))
for f in gabage:
	command = 'del /F /Q \"%s\"'%f
	if len(sys.argv) >= 3:
		print('just print: kill dup, execute - ' + command)
	else:
		print('kill dup, execute - ' + command)
		os.system(command)
