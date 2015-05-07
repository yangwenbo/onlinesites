from django.http import HttpResponse
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_protect
import datetime,hashlib,os,subprocess
from myapp.models import sample
from django.core.servers.basehttp import FileWrapper
import threading
'''
class dynThread(threading.Thread):
	
	def __init__(self, p,upfile,dynamic_loc):
		threading.Thread.__init__(self)
		self.p = p
		self.upfile = upfile
		self.dynamic_loc = dynamic_loc

	def run(self):
		print "aaa"
		run_dynamic_analysis(self.p,self.upfile,self.dynamic_loc)
'''


cur_dir = os.path.split(os.path.realpath(__file__))[0]
print cur_dir
path = os.getcwd()
up_loc = path+"/files/%s/upload/"


def hello(request):
	return HttpResponse("hello world aa")


def static(request):
	return render_to_response('static.html')


def uploadapk(request):
	if 'file' in request.FILES:
		f = request.FILES['file']
		apkhash = hashlib.md5(f.read()).hexdigest()
		try:
			p = sample.objects.get(md5hash = apkhash)
		except sample.DoesNotExist:
			handle_uploaded_file(f,apkhash,'s')
			#static_analysis(apkhash)
			return render_to_response('static.html',{'success':True})
		except sample.MultipleObjectsReturned:
			return render_to_response('static.html',{'error':'internalerror'})
		else:
			return static_res(request,apkhash)
	else:
		return render_to_response('static.html',{'error':'nofile'})


def handle_uploaded_file(f,h,flag='n'):
	#cal hash, create app folder, upload folder, write database

	upload_loc = up_loc % h
	if not os.path.exists(upload_loc):
		os.makedirs(upload_loc)
	fn = upload_loc + f.name
	des = open(fn,'wb')
	for chunk in f.chunks():
		des.write(chunk)
	des.close()

	try:
		p = sample.objects.get(md5hash=h)
	except sample.DoesNotExist:
		if os.path.isfile(fn):
			s = sample(md5hash = h,
				upload_location = fn,
				upload_time = datetime.datetime.now(),
				static_status = 0,
				dynamic_status = 0,
				manual_status = 0)
			s.save()
	else:
		if os.path.isfile(fn):
			p.upload_location=fn
			p.upload_time=datetime.datetime.now()
			s.save()
	'''
	if flag == 's':
		static_analysis(h)
	if flag == 'd':
		#subprocess.Popen(["sleep","100"])
		dynamic_analysis(h)
	'''


def static_res(request,offset):
	try:
		p = sample.objects.get(md5hash = offset)
	except sample.DoesNotExist:
		return render_to_response('static.html',{'error':'nofile'})
	except sample.MultipleObjectsReturned:
		return render_to_response('static.html',{'error':'internalerror'})
	else:
		fn = p.static_location
		if fn and os.path.isfile(fn):
			with open(fn, 'r') as f:
				lines = f.readlines()
			return render_to_response("static_res.html",{'lines':lines})
		else:
			return render_to_response('static.html',{'error':'nofile'})
			#static_analysis(offset)
			#return render_to_response('static.html',{'analyzing':True})



def result(request):
	p = sample.objects.all()
	if len(p) == 0:
		return render_to_response('result.html',{'resexist':False})
	else:
		return render_to_response('result.html',{'resexist':True, 'item_list':p})

def dynamic(request):
	return render_to_response('dynamic.html')


def uploadhash(request):
	if not 'hash' in request.POST:
		return render_to_response('static.html')
	apkhash = request.POST['hash']
	if apkhash:
		return static_res(request,apkhash)
	else:
		return render_to_response('static.html',{'error':'nohash'})

def uploadhash_d(request):
	if not 'hash' in request.POST:
		return render_to_response('dynamic.html')
	apkhash = request.POST['hash']
	if apkhash:
		return dynamic_res(request,apkhash)
	else:
		return render_to_response('dynamic.html',{'error':'nohash'})


def uploadapk_d(request):
	if 'file' in request.FILES:
		f = request.FILES['file']
		apkhash = hashlib.md5(f.read()).hexdigest()
		try:
			p = sample.objects.get(md5hash = apkhash)
		except sample.DoesNotExist:
			handle_uploaded_file(f,apkhash,'d')
			
			#dynamic_analysis(apkhash)
			return render_to_response('dynamic.html',{'success':True})
		except sample.MultipleObjectsReturned:
			return render_to_response('dynamic.html',{'error':'internalerror'})
		else:
			return dynamic_res(request,apkhash)
	else:
		return render_to_response('dynamic.html',{'error':'nofile'})

def dynamic_res(request,offset):
	try:
		p = sample.objects.get(md5hash = offset)
	except sample.DoesNotExist:
		return render_to_response('dynamic.html',{'error':'nofile'})
	except sample.MultipleObjectsReturned:
		return render_to_response('dynamic.html',{'error':'internalerror'})
	else:
		dy_fn = p.dynamic_location
		if dy_fn:
			if os.path.isfile(dy_fn):
				with open(dy_fn, 'r') as f:
					lines = f.readlines()
				return render_to_response("static_res.html",{'lines':lines})
			else:
				return render_to_response('dynamic.html',{'error':'internalerror'})
		else:
			return render_to_response('dynamic.html',{'error':'nofile'})
			#dynamic_analysis(offset)
			#return render_to_response('dynamic.html',{'analyzing':True})

def manual_res(request,offset):
	try:
		p = sample.objects.get(md5hash = offset)
	except sample.DoesNotExist:
		return render_to_response('dynamic.html',{'error':'nofile'})
	except sample.MultipleObjectsReturned:
		return render_to_response('dynamic.html',{'error':'internalerror'})
	else:
		ma_fn = p.manual_location
		if ma_fn:
			if os.path.isfile(ma_fn):
				wrapper = FileWrapper(file(ma_fn))
				response = HttpResponse(wrapper, content_type='application/zip')
				response['Content-Length'] = os.path.getsize(ma_fn)
				response['Content-Disposition'] = "attachment;filename=%s" % (offset+"_manual.tar.gz")
				return response
			else:
				return render_to_response('dynamic.html',{'error':'internalerror'})
		else:
			return render_to_response('dynamic.html',{'error':'nofile'})


def download_res(request,offset):
	try:
		p = sample.objects.get(md5hash = offset)
	except sample.DoesNotExist:
		return render_to_response('dynamic.html',{'error':'nofile'})
	except sample.MultipleObjectsReturned:
		return render_to_response('dynamic.html',{'error':'internalerror'})
	else:
		dl_fn = p.download_location
		if dl_fn:
			if os.path.isfile(dl_fn):
				wrapper = FileWrapper(file(dl_fn))
				response = HttpResponse(wrapper, content_type='application/zip')
				response['Content-Length'] = os.path.getsize(dl_fn)
				response['Content-Disposition'] = "attachment;filename=%s" % (offset+"_dynamic.tar.gz")
				return response
			else:
				return render_to_response('dynamic.html',{'error':'internalerror'})
		else:
			return render_to_response('dynamic.html',{'error':'nofile'})
			#dynamic_analysis(offset)
			#return render_to_response('dynamic.html',{'analyzing':True})







def dynamic_analysis(apkhash):
	dynamic_loc = "files/"+apkhash+"/dynamic/"
	if not os.path.exists(dynamic_loc):
		os.makedirs(dynamic_loc)
	#fn = dynamic_loc + apkhash+".txt"
	p = sample.objects.get(md5hash = apkhash)
	upfile = p.upload_location
	#need to check upload file is fine!!!!!!!!!!!!
	if upfile and os.path.isfile(upfile):
		try:
			#thread.start_new_thread(run_dynamic_analysis,(p,upfile,dynamic_loc,))
			print "eee"
			print p
			print upfile
			print dynamic_loc
			'''
			dt = dynThread(p,upfile,dynamic_loc)
			dt.setDaemon(True)
			print "yyyyyyyyy"
			dt.start()
			print "xxxx"
			'''
			test()
			
			a = render_to_response('dynamic.html',{'success':True})
			print "aaaaaaaaaa"
			return a
			
		except:
			return render_to_response('dynamic.html',{'error':'internalerror'})
			
		'''
		subprocess.call(["python",cur_dir+"/apkanalysis/conf/all.py",upfile,dynamic_loc])
		dy_fn = dynamic_loc + "parseRes/behavior"
		dl_fn = dynamic_loc + "download.zip"
		if os.path.isfile(dy_fn):
			p.dynamic_location = dy_fn
			p.dynamic_time = datetime.datetime.now()
			p.save()
		if os.path.isfile(dl_fn):
			p.download_location = dl_fn
			p.save()
		'''

def run_dynamic_analysis(p,upfile,dynamic_loc):
	subprocess.call(["python",cur_dir+"/apkanalysis/conf/all.py",upfile,dynamic_loc])
	print "#################################################################################################################"
	dy_fn = dynamic_loc + "parseRes/behavior"
	dl_fn = dynamic_loc + "download.zip"
	if os.path.isfile(dy_fn):
		p.dynamic_location = dy_fn
		p.dynamic_time = datetime.datetime.now()
		p.save()
	if os.path.isfile(dl_fn):
		p.download_location = dl_fn
		p.save()





def static_analysis(apkhash):
	static_loc = "files/"+apkhash+"/static/"
	if not os.path.exists(static_loc):
		os.makedirs(static_loc)
	fn = static_loc + apkhash+".txt"
	p = sample.objects.get(md5hash = apkhash)
	upfile = p.upload_location
	#need to check upload file is fine!!!!!!!!!!!!
	if upfile and os.path.isfile(upfile):
		subprocess.call(['python',os.path.dirname(__file__)+'/apkanalysis/static.py',upfile,fn])
		
		if os.path.isfile(fn):
			p.static_location = fn
			p.static_time = datetime.datetime.now()
			p.save()
