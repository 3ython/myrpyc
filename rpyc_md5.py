# -*- coding: utf-8 -*-

import os
import sys
import time
import hashlib
import rpyc

def run():
    import hashlib
    md5 = hashlib.md5()
    with open(u'listfile.txt','rb') as listfile:
        for filename in iter(lambda: listfile.readline(), ''):
            try:
                with open(filename.rstrip(),'rb') as f:
                    for chunk in iter(lambda: f.read(8192), ''):
                        md5.update(chunk)
                        print md5.hexdigest()
            except IOError, e:
                print e
                continue

if __name__ == '__main__':
    
    SERVER = raw_input('enter Rpyc server ip:')
    conect = rpyc.classic.connect(SERVER)
#    conect.modules.__builtin__.run = run
#    conect.execute("run()")
#    print conect
    
    conect.execute("""def run(fileobj, fileobjsize):
            import hashlib
            import os
            md5 = hashlib.md5()
            print 'name: ', fileobj.name
            print 'size: ', fileobjsize,  'mb'
            
            with fileobj as f:
                for chunk in iter(lambda: f.read(8192), ''):
                    md5.update(chunk)
                print md5.hexdigest()
                print '' """)

                

    with open(u'listfile.txt','rb') as listfile:
        for filename in iter(lambda: listfile.readline(), ''):
                try:
                    conect.modules.__builtin__.fileobj     = open(filename.rstrip(),'rb')
                    conect.modules.__builtin__.fileobjsize = os.stat(filename.rstrip())[6]/1024.0/1024
                    conect.execute("run(fileobj, fileobjsize)")
                except IOError, e:
                    print e
                    continue
                    