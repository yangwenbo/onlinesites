#!/usr/bin/env python
# encoding: utf-8
import MySQLdb,time,datetime,subprocess,os
'''
static_status
0: not analysis
1: analysis ok
2: something wrong
'''





no_static = "SELECT * FROM myapp_sample where static_status = 0"
static_ok = "UPDATE myapp_sample SET static_status = 1, static_location = \'%s\', static_time = now() WHERE ID = %d"
static_error = "UPDATE myapp_sample SET static_status = 2 WHERE ID = %d"
path = os.getcwd()
s_loc = path+"/files/%s/static/"

def static_analysis(apkhash,uploc):
	static_loc = s_loc % apkhash
	if not os.path.exists(static_loc):
		os.makedirs(static_loc)
	fn = static_loc + apkhash+".txt"
	if uploc and os.path.isfile(uploc):
		print os.getcwd()
		print fn
		print uploc
		subprocess.call(['python',path+'/mysite/apkanalysis/static.py',uploc,fn])
		return fn
	else:
		return ""



def main():
	while True:
		db = MySQLdb.connect("localhost","root","root","indroid")
		try:
			cursor = db.cursor()
			cursor.execute(no_static)
			result = cursor.fetchone()
			print result
			static_id = result[0]
			md5hash = result[2]
			upload_location = result[3]
			print static_id
			print md5hash
			print upload_location
			static_res = static_analysis(md5hash,upload_location)
			print static_res
			if static_res and os.path.isfile(static_res):
				try:
					sok = static_ok % (static_res, int(static_id))
					cursor.execute(sok)
					db.commit()
				except Exception,e:
					print e
					print "commit error"
					db.rollback()
				
			else:
				try:
					serr = static_error %  int(static_id)
					cursor.execute(serr)
					db.commit()
				except Exception,e:
					print e
					print "commit error"
					db.rollback()
		except Exception,e:
			print e
			db.close()
			print "no static"
			time.sleep(10)
			print "sleep over"
			continue
		else:
			db.close()
			print "else"
			continue




if __name__ == "__main__":
	#pass
	main()
