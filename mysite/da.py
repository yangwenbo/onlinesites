#!/usr/bin/env python
# encoding: utf-8

import MySQLdb,time,datetime,subprocess,os,threading
'''
static_status
0: not analysis
1: analysis ok
2: doing
3: something wrong

indroid device: serial_num:(status,last_time)
'''

FIND_FREE_DEVICE = 15
FIND_NEW_TASK = 15
MAX_RUNTIME = 120


indroid_device = {
	'0149C25E0A00C005': [0,0],
	'0090fd6dde218518': [0,0],
}
'''
0: free
1: busy
'''

#subprocess.call(["python",cur_dir+"/apkanalysis/conf/all.py",upfile,dynamic_loc])
#python all.py XXX.apk outDir serialnum
#python ~/djangotest/mysite/mysite/apkanalysis/conf/allstart.py ~/tools/android/apksample/lbdDemo.apk ./lbd 0149C25E0A00C005



no_dynamic = "SELECT * FROM myapp_sample where dynamic_status = 0"
dynamic_ok = "UPDATE myapp_sample SET dynamic_status = 1, dynamic_location = \'%s\', download_location = \'%s\', dynamic_time = now() WHERE ID = %d"
dynamic_error = "UPDATE myapp_sample SET dynamic_status = 3 WHERE ID = %d"
dynamic_doing = "UPDATE myapp_sample SET dynamic_status = 2 WHERE ID = %d"

path = os.getcwd()
d_loc = path+"/files/%s/dynamic/"

class dyn_Thread (threading.Thread):
	def __init__(self,dy_id,apkhash,uploc,sn):
		threading.Thread.__init__(self)
		print "init thread"
		self.db = MySQLdb.connect("localhost","root","root","indroid")
		self.cursor = self.db.cursor()
		self.dy_id = dy_id
		self.hash = apkhash
		self.sn = sn
		self.uploc = uploc

	def run(self):
		print "run thread"
		self.start_time = time.time()
		dynamic_loc = d_loc % self.hash
		if not os.path.exists(dynamic_loc):
			os.makedirs(dynamic_loc)
		if self.uploc and os.path.isfile(self.uploc):
			print 'python '+path+'/mysite/apkanalysis/conf/allstart.py '+ self.uploc+" "+dynamic_loc+" "+self.sn
			subprocess.call(['python',path+'/mysite/apkanalysis/conf/allstart.py',self.uploc,dynamic_loc,self.sn])
			indroid_device[self.sn][0] = 0
			dy_fn = dynamic_loc + "parseRes/behavior"
			dl_fn = dynamic_loc + "download.zip"
			if os.path.isfile(dy_fn) and os.path.isfile(dl_fn):
				try:
					dok = dynamic_ok % (dy_fn, dl_fn, int(self.dy_id))
					self.cursor.execute(dok)
					self.db.commit()
				except Exception,e:
					print e
					print "commit error in dynamic ok"
					self.db.rollback()
				finally:
					self.db.close()
			else:
				if not os.path.isfile(dy_fn):
					print "no dynamic res"
				if not os.path.isfile(dl_fn):
					print "no download res"
				try:
					derr = dynamic_error %  int(self.dy_id)
					self.cursor.execute(derr)
					self.db.commit()
				except Exception,e:
					print e
					print "commit error in print dynamic error"
					self.db.rollback()
				finally:
					self.db.close()
		else:
			print "no upload apk in dynamic analysis"
			try:
				derr = dynamic_error %  int(self.dy_id)
				self.cursor.execute(derr)
				self.db.commit()
			except Exception,e:
				print e
				print "commit error"
				self.db.rollback()
			finally:
				self.db.close()






def is_free():
	s = subprocess.Popen(['adb',"devices"],stdout=subprocess.PIPE)
	dv = s.stdout.read().split('\n')[1:]
	realdv = []
	for d in dv:
		tmp = d.split('\t')
		if d and len(tmp) == 2 and tmp[1] == 'device':
			realdv.append(tmp[0])


	cur_time = time.time()
	for i in indroid_device:
		if cur_time - indroid_device[i][1] > MAX_RUNTIME:
			indroid_device[i][0] = 0

	for rd in realdv:
		if indroid_device.has_key(rd) and indroid_device[rd][0] == 0:
			print rd+" is free"
			indroid_device[rd][0] = 1
			indroid_device[rd][1] = cur_time
			return rd
	return 0



def main():
	while True:
		db = MySQLdb.connect("localhost","root","root","indroid")
		try:
			cursor = db.cursor()
			cursor.execute(no_dynamic)
			result = cursor.fetchone()
			print result
			dynamic_id = result[0]
			md5hash = result[2]
			upload_location = result[3]

			try:
				dydoing = dynamic_doing %  int(dynamic_id)
				cursor.execute(dydoing)
				db.commit()
			except Exception,e:
				print e
				print "commit error in setting dynamic doing"
				db.rollback()
			while True:
				device_serial = is_free()
				if device_serial:
					break; 
				print "no resource is free"
				time.sleep(FIND_FREE_DEVICE)
			newthread = dyn_Thread(dynamic_id,md5hash, upload_location, device_serial)
			newthread.start()
		except Exception,e:
			print e
			print "no dynamic"
			db.close()
			time.sleep(FIND_NEW_TASK)
			print "sleep over"
			continue
		else:
			db.close()
			print "else"
			continue


	

if __name__ == "__main__":
	main()
	#test()
