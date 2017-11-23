import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import datetime
import json
import os
import time
import numpy as np
import traceback
import matplotlib.pyplot as plt
import sys
import modelHandler 

config=json.load(open("./torcs_central/config.json"))
resourcePath=config['resourcePath']
imagePath=config['imagePath']
tempPath=config['tempPath']

centralModel = modelHandler.CentralModel()
#---------------create necessary directories-----------------------------#
if not os.path.isdir(resourcePath):
    os.mkdir(resourcePath)
    print("Directory created at ",resourcePath)

if not os.path.isdir(imagePath):
    os.mkdir(imagePath)
    print("Directory created at ",imagePath)

if not os.path.isdir(tempPath):
    os.mkdir(tempPath)
    print("Directory created at ",tempPath)    

#---------------Start browser session-----------------------------#
try:
    os.system("sensible-browser http://localhost:{} &".format(config['port']))
except Exception as e:
    print("Could not open browser")

global resource
resource=[]

log=[]

workers = []
global episode_count
episode_count=0

global rewards
rewards = []

global episodes
episodes = []

statusLog=[]

parameterDict=config

try:
    parameterDict.pop('clientID')
    parameterDict.pop('pulledModels')
except:
    print("check config.json")

#-------------------- Update time -------------------------------------#
startTime=datetime.datetime.now()
upTime=0.0

def updateUpTime():
    upTime=(datetime.datetime.now()-startTime).seconds
    mm,ss = divmod(upTime,60)
    hh,mm = divmod(mm,60)
    upTime = "{:02d}:{:02d}:{:02d}".format(hh,mm,ss)
    # upTime.strftime("%M:%S")
    return upTime

#-------------------- Update Users or Workers -------------------------------------#
def updateUsers():
    for log_ in log:
        worker = log_[0]
        if worker not in workers:
            workers.append(worker)

print("running from:",os.getcwd())

#-------------------- set limit on length of logs -------------------------------------#
def limitLog(limitLog_=50,limitStatusLog=20):
    if len(log)>limitLog_:
        log.pop(0)
    if len(statusLog)>limitStatusLog:
        statusLog.pop(0)    

#-------------------- StatusHandler -------------------------------------#
def statusHandler(metaData):
    status_str=''
    if metaData['cmd']=='updateResource':
        status_str+="Worker {} Ended game at {}".format(metaData['clientID'],updateUpTime())
        statusLog.append(status_str)
    elif metaData['cmd']=='fetchResource':
        status_str+="Worker {} Started game at {}".format(metaData['clientID'],updateUpTime())
        statusLog.append(status_str)
    else:
        pass
#-------------------- Plotter -------------------------------------#
global plotterStarttime
plotterStarttime=datetime.datetime.now()
def plotter(refreshRate=5):
    if (datetime.datetime.now()-plotterStarttime).seconds > refreshRate:
        global plotterStarttime
        plotterStarttime = datetime.datetime.now()
        if len(episodes)>0 and len(rewards)>0:
            plt.plot(episodes,rewards)
            plt.xlabel('no of episodes')
            plt.ylabel('no of rewards')
            plt.title('performance')
            plt.savefig(os.path.join(imagePath,'test1.png'))
#-------------------- Handlers -------------------------------------#
def handlerequest(request):
    cmd=request['cmd']
    if cmd=='ping':
        return json.dumps({"response":"ping_success","status":0})
    elif cmd=='updateResource':
        return json.dumps({"response":"update_success","status":0})
    elif cmd=='fetchResource':
        return json.dumps({"response":"update_success","status":0,"data":resource})
    else:
        return request

class Download(tornado.web.RequestHandler):
    def get(self,key):
        if os.path.exists(os.path.join(resourcePath,'actor.h5')) and os.path.exists(os.path.join(resourcePath,'critic.h5')):
            filename = self.get_arguments('file',True)[0]
            if filename=='actor':
                with open(os.path.join(resourcePath,'actor.h5'),'rb') as fp:
                    fileData = fp.read()
                self.write(fileData)
            elif filename=='critic':
                with open(os.path.join(resourcePath,'critic.h5'),'rb') as fp:
                    fileData = fp.read()
                self.write(fileData)
            else:
                self.write(json.dumps({"actor":None,"critic":None}))
            # with open(os.path.join(resourcePath,'critic.h5')) as fp:
            #     criticData = fp.read()
            # self.write(json.dumps({"actor":open(os.path.join(resourcePath,'actor.h5')),"critic":open(os.path.join(resourcePath,'critic.h5'))}))
        else:
            self.write(json.dumps({"actor":None,"critic":None}))


class Upload(tornado.web.RequestHandler):
    def post(self):
        print(self.request.files['actor'][0].keys())
        print(self.request.files['critic'][0].keys())
        actor_body = self.request.files['actor'][0]['body']
        critic_body = self.request.files['critic'][0]['body']
        with open(os.path.join(tempPath,'actor.h5'),'wb') as fp:
            fp.write(actor_body)
        with open(os.path.join(tempPath,'critic.h5'),'wb') as fp:
            fp.write(critic_body)
        self.write(json.dumps({"response":"update_success","status":0}))
        centralModel.updateWeights()    
        

class MyHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        global resource
        resource.append(data)
        try:
            log.append([data['clientID'],data['cmd'],time.ctime()])
            statusHandler(data)
            try:
                if ('episode_done' in data['data'].keys()) and ('total_reward' in data['data'].keys()):
                    global episode_count
                    episode_count+=1
                    episodes.append(episode_count)
                    rewards.append(data['data']['total_reward'])
            except Exception as e:
                traceback.print_exc(e)
                print("error in metaData") 
                pass

        except Exception as e:
            traceback.print_exc(e)
            print("no clientID")
        self.write(handlerequest(data))

    def get(self):
        updateUsers()
        updateUpTime()
        limitLog()
        plotter()
        self.render("template.html", 
            title="TORCS_A3C", 
            items=log, 
            workers=workers,
            maxReward=[max(rewards) if len(rewards)>0 else 0 for r in range(1)],
            maxEpisodes=[max(episodes) if len(episodes)>0 else 0 for ep in range(1)],
            upTime=updateUpTime(),
            testParams=parameterDict,
            statusLog=statusLog)    

if __name__ == '__main__':
    settings = {
        "debug": True,
        "template_path": os.path.join(os.getcwd(),"torcs_central","templates"),
        "static_path": os.path.join(os.getcwd(),"torcs_central","templates")
        }
    app = tornado.web.Application([ 
        tornado.web.url(r'/', MyHandler),
        tornado.web.url(r'/upload', Upload) ,
        tornado.web.url(r'/download/(.*)', Download) ],**settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9090)
    print('Starting server on port 9090')
    tornado.ioloop.IOLoop.instance().start()