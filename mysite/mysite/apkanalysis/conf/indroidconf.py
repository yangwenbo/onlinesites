#!/usr/bin/env python
import os,sys,subprocess
import conf




opt = sys.argv[1]
APKFile = sys.argv[2]
package = sys.argv[3]
adbPath = sys.argv[4]
print opt
print APKFile
print package
print adbPath

'''
perms,apis,all,def,mal
'''

cur_dir = os.path.split(os.path.realpath(__file__))[0]
#os.chdir("./config")
#os.popen("./gen_class_dlist.sh "+sys.argv[1]+" " + sys.argv[2])
conf_dir = cur_dir+"/"+opt+"_classmethod/"
if not opt.startswith("def"):
	subprocess.call("python "+cur_dir+"/gen_cm_"+opt+".py " + APKFile,shell=True)
	subprocess.call(adbPath + "push "+conf_dir+package+"_method.dlist /data/data/"+package+"/method.dlist", shell=True)
	subprocess.call(adbPath + "push "+conf_dir+package+"_class.dlist /data/data/"+package+"/class.dlist", shell=True)
else:
	subprocess.call("python "+cur_dir+"/gen_cm_all.py "+ APKFile, shell=True)
	subprocess.call(adbPath + "push all_classmethod/"+package+"_class.dlist /data/data/"+package+"/class.dlist", shell=True)
subprocess.call(adbPath + "push "+cur_dir+"/config/flag.dlist /data/data/"+package+"/", shell=True)
subprocess.call(adbPath + "push "+cur_dir+"/config/object.dlist /data/data/"+package+"/", shell=True)
subprocess.call(adbPath + "push "+cur_dir+"/config/unpack.dlist /data/data/"+package+"/", shell=True)

