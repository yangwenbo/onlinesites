#!/usr/bin/env python
import subprocess
import sys
import os
import conf
sys.path.append("/home/ywb/tools/androguard/")
from androguard.core.bytecodes import apk

adbPath = conf.adbPath
option = conf.autoconf
'''
option can be perms, apis, all, def.
perms: monitor sensitive permissions api
apis: monitor specific apis which can be configure in 'sensitive_api/sensitive_method'
all: monitor all methods in apks(which may cause heavy overhead
def: just monitor function call and object
'''
cur_dir = os.path.split(os.path.realpath(__file__))[0]
APKFile = sys.argv[1]
subprocess.call(adbPath + "install " + APKFile, shell=True)
subprocess.call(adbPath + "shell chmod 664 /data/system/packages.list", shell=True)
a = apk.APK(APKFile)
p = a.get_package()
subprocess.call(["python", cur_dir+"/indroidconf.py", option, APKFile,p])
ma = a.get_main_activity()
subprocess.call(adbPath + "shell am start "+p+"/"+ma, shell=True)
subprocess.call(adbPath + "shell monkey -p " + p + "  -s 500 --monitor-native-crashes -v -v -v 1000", shell=True)
if len(sys.argv) == 3:
	path = sys.argv[2]
	subprocess.call("python "+cur_dir+"/pullfile.py "+APKFile+" "+path, shell=True)
	subprocess.call("zip -r "+path+"/download.zip "+path, shell=True)
else:
	subprocess.call("python "+cur_dir+"/pullfile.py "+APKFile, shell=True)
subprocess.call(adbPath + "uninstall " + p, shell=True)

