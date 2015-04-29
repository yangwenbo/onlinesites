#!/usr/bin/env python

import os,sys,subprocess,hashlib

sys.path.append("/home/ywb/tools/androguard")
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis import analysis
import conf
#adbPath = "adb "

cur_dir = os.path.split(os.path.realpath(__file__))[0]
print sys.argv[1]
print sys.argv[2]
print sys.argv[3]

if __name__ == '__main__':
	APKFile = sys.argv[1]
	adbPath = sys.argv[2]
	a = apk.APK(APKFile)
	p = a.get_package()
	with open(APKFile, 'rb') as f:
		hashMD5 = hashlib.md5()
		hashMD5.update(f.read())
		fileMD5 = hashMD5.hexdigest()
	
	ndir = "../dynam_out/"+fileMD5
	if len(sys.argv) == 4:
		dataDir = sys.argv[3]
	if len(sys.argv) == 3:
		dataDir = ndir + "/data" 
	if not os.path.exists(dataDir):
		os.makedirs(dataDir)
	subprocess.call(adbPath + "pull /data/data/"+p + " " + dataDir, shell=True)
	subprocess.call(["python",cur_dir+"/parseIndroidRes.py",dataDir])
	subprocess.call(["python",cur_dir+"/parseMal.py",APKFile,dataDir])
	#x = os.popen("./parseIndroidRes.py "+dataDir)
	#print type(x)
	#os.popen("./parseMal.py "+APKFile+" "+dataDir)
