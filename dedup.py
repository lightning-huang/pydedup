#coding=utf-8
import os,sys,hashlib
from os.path import join,getsize

picked_size = 1024000

def mark_gabage(l, file, seed):
    l.append(file)
    if seed == None:
        print('empty-file-gabage found: %s'%file)
    else:
        print('same as %s, gabage found: %s'%(seed,file))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USAGE: python dedup.py {directory} {anystringtojustprint}')
        sys.exit(-1)
    hash_repo = {}
    gabage = []
    systemerrorfiles = []
    for root, dirs, files in os.walk(sys.argv[1]):
        if len(files) > 0:
            for file in files:
                full_path = join(root,file)
                file_size = getsize(full_path)
                if file_size <= 0:
                    mark_gabage(gabage, full_path, None)
                    continue
                try:
                    f = open(full_path,'rb')
                    bytesfromfile = f.read(picked_size)
                    f.close()
                    current_md5 = hashlib.md5()
                    current_md5.update(bytesfromfile)
                    current_md5.update(('%s'%file_size).encode('UTF-8'))
                    current_md5_hex = current_md5.hexdigest()
                    if current_md5_hex in hash_repo.keys():
                        existing = hash_repo[current_md5_hex]
                        if len(existing) <= len(full_path):
                            mark_gabage(gabage, full_path, existing)
                        else:
                            mark_gabage(gabage, existing, full_path)
                            hash_repo[current_md5_hex] = full_path
                    else:
                        hash_repo[current_md5_hex] = full_path
                        print('keep %s'%full_path)
                except:
                    print('meet system error for %s'%full_path) 
                    systemerrorfiles.append(full_path)

    print("gabage summary")
    print("gabage entry amount: %s"%len(gabage))
    if len(systemerrorfiles) > 0:
        print('system error files amount: %s'%len(systemerrorfiles))

    size_released = 0.0
    for f in gabage:
        command = 'del /F /Q \"%s\"'%f
        if len(sys.argv) >= 3:
            print('just print: kill dup, execute - ' + command)
        else:
            print('kill dup, execute - ' + command)
            try:
                file_size_to_relase = getsize(f)
                os.system(command)
                print("execution success!")
                size_released += file_size_to_relase
            except:
                print("execution failed!")
    print('total release size: %.2f GB'%(size_released/1024/1024/1024))
