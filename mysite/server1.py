#!/usr/bin/env python

from SocketServer import TCPServer, StreamRequestHandler, ThreadingMixIn
import socket, threading, time, simplejson, os, subprocess, random, MySQLdb

CLIENT_APK_CACHE_NUM = 3
TODO_API_DIR = ''
clients = []
clients_status_dict = {}
HOST = ''
PORT = 12347
ADDR = (HOST, PORT)
#SQL_getDyToDo = "SELECT * FROM myapp_sample where dynamic_status = 1"
SQL_getDyToDo = "SELECT * FROM myapp_sample where manual_status = 0"
SQL_DySetDoing = "UPDATE myapp_sample SET manual_status = 2 WHERE ID = %d"
def get_todo_apk_list():
    return os.listdir('files/')
def show():
    of = file("system_status","w+")
    _ = os.system("clear")
    temp_dict = {}
    print '----------------------System Status--------------------------------\n'
    print 'Now %d '%len(clients) + 'clients connected\n'
    of.writelines( '----------------------System Status--------------------------------\n')
    of.writelines( 'Now %d '%len(clients) + 'clients connected\n')
    for i in clients:
        temp_dict = clients_status_dict[i]
        try:

            print 'Client IP:' + i + '\n'
            print 'Unfinished Task(' + str(temp_dict['unfinishedApkNum']) + '): ' + str(temp_dict['unfinishedApks']) + '\n'
            print 'Disk Usage: ' + temp_dict['disk_usage'] + '\n'
            print 'Memory Usage: ' + temp_dict['mem_usage'] + '\n'
            print 'CPU Usage: ' + temp_dict['cpu_usage'] + '\n'
            print '########################################################'

            of.writelines( '######################Client' + str(clients.index(i)) + '###########################')
            of.writelines( 'Client IP:' + i + '\n')
            of.writelines( 'Unfinished Task(' + str(temp_dict['unfinishedApkNum']) + '): ' + str(temp_dict['unfinishedApks']) + '\n')
            of.writelines( 'Disk Usage: ' + temp_dict['disk_usage'] + '\n')
            of.writelines( 'Memory Usage: ' + temp_dict['mem_usage'] + '\n')
            of.writelines( 'CPU Usage: ' + temp_dict['cpu_usage'] + '\n')

        except:
            return
def check_status():
    apklist = get_send_apks()
    #print apklist
    for i in clients:
        if((clients_status_dict[i]['unfinishedApkNum'] < CLIENT_APK_CACHE_NUM) and (len(apklist) > 0)):
            target = random.randint(0, len(apklist)-1)
            newtask_file = apklist[target]['file']
            newtask_id = apklist[target]['id']
            cmd = "scp " + newtask_file + " " + clients_status_dict[i]['username'] + "@" + str(i) + ":" + clients_status_dict[i]['pwd'] + '/todo/' + " >/dev/null"
            #print cmd + '\n'
            
            if os.system(cmd) == 0:
                apklist.pop(target)
                db = MySQLdb.connect("localhost","root","root","indroid")
                cursor = db.cursor()
                cmd = SQL_DySetDoing %  int(newtask_id)
                print cmd
                cursor.execute(cmd)
                db.commit()
                db.close()
                pass
                #cmd2 = "mv todo/" + newtask + " done/"
                #print cmd2 + '\n'
                #os.system(cmd2)
def get_send_apks():
    #TODO
    toDoApks = []
    db = MySQLdb.connect("localhost","root","root","indroid")
    cursor = db.cursor()
    cursor.execute(SQL_getDyToDo)
    result = cursor.fetchall()
    #print result
    for i in result:
        temp = {}
        temp['file'] = i[3]
        temp['id'] = i[0]
        toDoApks.append(temp)
    #print result
    db.close()
    return toDoApks
def get_send_target():
    #TODO
    return target
def send_file_to(file, to):
    cmd = "scp files/" + newtask + '/upload/*' + " " + clients_status_dict[i]['username'] + "@" + str(i) + ":" + clients_status_dict[i]['pwd'] + '/todo/' + " >/dev/null"
    #print cmd + '\n'
    #TODO pop task
    if os.system(cmd) == 0:
        pass
        #cmd2 = "mv todo/" + newtask + " done/"
        #print cmd2 + '\n'
        #os.system(cmd2)
class Server(ThreadingMixIn, TCPServer):
    pass

class MyRequestHandler(StreamRequestHandler):
    def handle(self):
        print '...connected from:', self.client_address
        clients.append(self.client_address[0])
        while True:
            try:
                data = self.request.recv(2048)
                #print self.client_address[0] + " Client sent : " + data
                temp_dict = simplejson.loads(data)
                temp_dict['socket'] = self.request
                if(temp_dict['type'] == 'system_info'):
                    clients_status_dict[self.client_address[0]] = temp_dict
            except:
                print "Clieut disconnected..."
                clients.remove(self.client_address[0])
                clients_status_dict.pop(self.client_address[0])
                return

class FlashThread(threading.Thread):
    def run(self):
        while True:
            show()
            check_status()
            time.sleep(5)


if __name__ == "__main__":
    flashthread  = FlashThread()
    flashthread.start()
    tcpServ = Server(ADDR, MyRequestHandler)
    print 'waiting for connection...'
    tcpServ.serve_forever()

