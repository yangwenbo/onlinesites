#!/usr/bin/env python
import subprocess,sys,os
import conf
sys.path.append("/home/ywb/tools/androguard/")
from androguard.core.bytecodes import apk


serialnum = ""
adbPath = "adb "

if len(sys.argv) > 2:
	path = sys.argv[2]
	if len(sys.argv) > 3:
		serialnum = sys.argv[3]
		adbPath = adbPath + "-s " + serialnum +" "

option = conf.autoconf

'''
option can be perms, apis, all, def.
perms: monitor sensitive permissions api
apis: monitor specific apis which can be configure in 'sensitive_api/sensitive_method'
all: monitor all methods in apks(which may cause heavy overhead
def: just monitor function call and object
'''

def pack(p):
	i = p.find("dynamic")
	cmd = "tar -zcvf "+p+"/download.tar.gz -C "+p[:i]+" "+p[i:]
	subprocess.call(cmd,shell=True)



cur_dir = os.path.split(os.path.realpath(__file__))[0]
APKFile = sys.argv[1]
subprocess.call(adbPath + "install " + APKFile, shell=True)
subprocess.call(adbPath + "shell chmod 664 /data/system/packages.list", shell=True)

a = apk.APK(APKFile)
p = a.get_package()
subprocess.call(["python", cur_dir+"/indroidconf.py", option, APKFile, p, adbPath])

ma = a.get_main_activity()
subprocess.call(adbPath + "shell am start "+p+"/"+ma, shell=True)
subprocess.call(adbPath + "shell monkey -p " + p + "  -s 500 1000", shell=True)
if len(sys.argv) > 2 :
	subprocess.call(["python",cur_dir+"/pullfile.py",APKFile,adbPath,path])
	#subprocess.call("zip -jr "+path+"/download.zip "+path, shell=True)
	pack(path)

else:
	subprocess.call(["python",cur_dir+"/pullfile.py",APKFile,adbPath])

subprocess.call(adbPath + "uninstall " + p, shell=True)
