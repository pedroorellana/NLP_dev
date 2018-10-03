#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
""" TecnoSmart Artificial Intelligence
AI Platform : Cluster Control for CLI
Created on 2018-07-10
@author: tmardesic
"""

import time, inspect, requests, json, html, base64, sys, os, redis, psutil
from celery import Celery


#app = Celery('tasks', backend='rpc://', broker='pyamqp://tsmai:tec1465@10.20.0.114//')
#nodes = ["10.20.0.114"]
nodes = ["127.0.0.1"]
# ps --forest $(ps -e --no-header -o pid,ppid|awk -vp=32313 'function r(s){print s;s=a[s];while(s){sub(",","",s);t=s;sub(",.*","",t);sub("[0-9]+","",s);r(t)}}{a[$2]=a[$2]","$1}END{r(p)}')
IP = "10.20.0.114"

noticia = 'El general director de Carabineros, Hermes Soto, manifestó \
este martes que respetan las medidas cautelares contra el ex jefe de \
Inteligencia Gonzalo Blu y el ex capitán Leonardo Osses, los que quedaron con arresto \
domicilario total y prisión preventiva, respectivamente, en el marco del caso Huracán. \
Al asistir al Congreso durante este martes, Soto dijo esperar que el juicio se realice lo antes \
posible para poder "seguir trabajando tranquilamente en la institución" y recalcó que "vamos a salir adelante". \
Incluso, sostuvo que tomarán las medidas ante situaciones irregulares en la institución "caiga quien caiga". \
El uniformado aseveró que "lo que puedo asegurar es que cada vez que ocurra una situación irregular, vamos a \
tomar las medidas administrativas de inmediato de eliminación y poner a las personas que se involucren en \
situaciones irregulares a disposición de los tribunales. Eso lo puedo asegurar, caiga quien caiga". \
"Esperemos que lo antes posible ya pueda ser desarrollado el juicio pertinente, que los fiscales terminen \
su investigación, que sea conocido por los tribunales respectivos no seguir con este tipo de temas en los \
medios de comunicación, en la opinión pública, que ningún beneficio provocan a la institución y se adopten \
las medidas que corresponden", reconoció. \
Soto aseveró que "a la institución para nada le beneficia que sigamos en este tipo de situaciones permanentemente".'


def kill():
    global IP
    def rpcKill(args):
        #os.sys.exit()
        import psutil
        print("Hola rpc()!! :"+str(os.getppid()))
        cmd = "kill -9 "        
        ll = list(filter(lambda x:  not len(x.cmdline())==0, psutil.process_iter()))
        for p in ll:
            print(p.cmdline())
        for p in list(filter(lambda x:  x.cmdline()[-1]=="./tsmai.py", ll)):
            cmd += " "+str(p.pid)
        os.system(cmd)
        return (1,2)
    callHtml(IP,rpcKill, ("","") )


# RPC mediante HTTP
def callHtml(ip,func,args):
    global IP
    _func,l  = inspect.getsourcelines(func)
    _func = "\n".join(list(map(lambda x:  x[_func[0].find("def"):], _func)))
    _func = base64.b64encode(_func.encode('utf-8')).decode("utf-8")
    _args = []
    for a in args:
        _args.append( base64.b64encode(a.encode('utf-8')).decode("utf-8")  if isinstance(a,str) else a)
    response = requests.post("http://"+IP+":20000", json={"func":_func,"args":str(tuple(_args))})
    jRespAI = json.loads(response.content.decode('utf-8'))
    hmsg = "[html]"+("[Err :"+str(jRespAI["code"])+"]" if jRespAI["code"]==1 else "[Ok]")
    printRemoteResponse(hmsg,str(html.unescape(jRespAI["ret"])))
    
    
def printRemoteResponse(hmsg="",s="",force=False):
    print("-"*30+" REMOTE RESPONSE --- "+hmsg+"-"*30) 
    print(str(type(s))+"  size_bytes:["+str(sys.getsizeof(s))+" : "+str(len(str(s)))+"]")
    if force==True:
        print(str(s))
    else:
        print( str(s)[0:40]+" ....... "+str(s)[len(str(s))-40:len(str(s))] if len(str(s))>80 else s)
    print("-"*97+"\n")


# RPC mediante Celery
def callCelery(task,args):
    #IP="10.20.0.114"
    #app = Celery('tasks', backend='rpc://', broker='pyamqp://tsmai:tec1465@'+IP+'//')
    app = Celery('tasks', backend='rpc://', broker='redis://10.20.0.114:6379/0')
    #time.sleep(100000)
    _task = app.send_task(task,args=[args],queue='result')
    #_task.wait()
    while not _task.ready():
        time.sleep(1)
        print("\nEsperando respuesta : "+task+ " .... _task_id:["+str(_task.task_id)+"] ... status:["+str(_task.status)+"]")
    r = _task.get()
    if isinstance(r,dict):
        if "code" in r.keys():
            hmsg = "[celery] "+("[Err :"+str(r["code"])+"]" if not r["code"]==0 else "[Ok]")
            printRemoteResponse(hmsg,r["ret"],True)
            return None
    printRemoteResponse("[Celery] [  Ok  ]",r)
    return r

    #===========================================================================
    # if True:
    #     print("Esperando respuesta....")
    #     #=======================================================================
    #     # time.sleep(10)
    #     # print("****************************")
    #     # time.sleep(10)
    #     #=======================================================================
    #     if _task.ready():
    #         r = _task.get()
    #         if isinstance(r,dict):
    #             if "code" in r.keys():
    #                 hmsg = "[celery] "+("[Err :"+str(r["code"])+"]" if r["code"]==1 else "[Ok]")
    #                 printRemoteResponse("celery","",r["ret"])
    #                 return
    #         printRemoteResponse("celery","",r)
    #         return r
    #===========================================================================


def update():
    global IP
    """ Actualizo el codigo remoto y reinicio """
    apfs = ["celeryconfig.py","DLakeModel.py","DLakeEtl.py","Log.py","tsmai.py","start-tsmai.sh"]
    for apf in apfs:
        with open(apf) as f:
            content  = f.read()
        def rpcUpdate(args):
            apf , content = args
            with open(apf,"w") as f:
                f.write(content)
            if apf.endswith(".sh"):
                os.system("chmod 777 "+apf)
            return "Ok: rpcUpdate : file:["+apf+"]  len:["+str(len(content))+"]"
        callHtml(IP,rpcUpdate, (apf, content) )

# ??????????????????
# ?????????????????? PARA VER TASKs REGISTRADAS ????
def registeredTasks():
    from celery.task.control import  inspect
    from itertools import chain
    i = inspect()
    i.registered_tasks()
    print(set(chain.from_iterable( i.registered_tasks().values() )))
    

def redisKeys(patern):
    redisCli = redis.StrictRedis(host='10.20.0.114',port=6379) #Redis(app.conf.CELERY_REDIS_HOST+":"+str(app.conf.CELERY_REDIS_PORT))
    #redisCli.set('test_key1', 'test_v3453534alue')
    #print(redisCli.get("test_key"))
    print(list(map(lambda x: x.decode("utf-8") ,redisCli.keys(patern))))
    
    redisCli.connection_pool.disconnect()


def help():
    pass


def isIpv4(ip):
    match = re.match("^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})$", ip)
    if not match:
        return False
    quad = []
    for number in match.groups():
        quad.append(int(number))
    if quad[0] < 1:
        return False
    for number in quad:
        if number > 255 or number < 0:
            return False
    return True

def get_network():
    network = psutil.net_io_counters(pernic=True)
    ifaces = psutil.net_if_addrs()
    networks = list()
    for k, v in ifaces.items():
        ip = v[0].address
        data = network[k]
        ifnet = dict()
        ifnet['ip'] = ip
        ifnet['iface'] = k
        ifnet['sent'] = '%.2fMB' % (data.bytes_sent/1024/1024)
        ifnet['recv'] = '%.2fMB' % (data.bytes_recv/1024/1024)
        ifnet['packets_sent'] = data.packets_sent
        ifnet['packets_recv'] = data.packets_recv
        ifnet['errin'] = data.errin
        ifnet['errout'] = data.errout
        ifnet['dropin'] = data.dropin
        ifnet['dropout'] = data.dropout
        networks.append(ifnet)
    return networks


if __name__ == '__main__':
    """ MAIN """
    a =  sys.argv
    
    #for n in get_network():
    #    if isIpv4(n["ip"]):
    #        print(n["ip"])
    
    ##callCelery("add",2)
    ##os.sys.exit()
    
    #app = Celery('tasks', backend='rpc://', broker='pyamqp://tsmai:tec1465@10.20.0.114//')
    
    #app = Celery('tasks', backend='redis://10.20.0.114:6379', broker='redis://10.20.0.114:6379')
    
    #time.sleep(1000)
    #route = app.amqp.routes#[0].route_for_task("tasks.nlp_news_cooperativa_sup300ch_LSASVDSKL")
    #print(route)
    #os.sys.exit()
    
    if a[1]=="update":
        update()
    elif a[1]=="redis":
        if a[2]=="keys":
            try:
                redisKeys(a[3])
            except:
                redisKeys("*")
    elif a[1]=="info" and a[2]=="tasks":
        registeredTasks()
    elif a[1]=="call" and a[2]=="nlp_news_cooperativa_sup300ch_TFIDFWB":
        callCelery(a[2],{"txt":a[3],"param":"nw5000"})#tuple(a[2:len(a)]))
    elif a[1]=="call" and a[2]=="nlp_news_cooperativa_sup300ch_LSASVDSKL":
        #while True:
        a[3] = noticia
        tfidfwb = "nlp_news_cooperativa_sup300ch_TFIDFWB"
        txtVec = callCelery(tfidfwb,{"txt":a[3],"param":"nw5000"})
        callCelery(a[2],{"txtVec":txtVec,"param":"nw5000"})#tuple(a[2:len(a)]))
    elif a[1]=="call" and a[2]=="add":
        callCelery(a[2],2)#tuple(a[2:len(a)]))
    elif a[1]=="kill":
        kill()
    else:
        print("Comando no encontrado.")
        
#task = app.send_task('add', args=[3, 5])
#print(task.get())

jIn = {"txt":["Hola Mundo"],"dLake":["nlp/news/cooperativa"],"dSet":["sup300ch"],"model-vec":["TFIDFWB"],\
       "model":["LSA"],"mParam":["svd100"],"vParam":["nw5000"]}
#=============================================================================== 
# jIn = {"txt":["Hola Mundo"],"dLake":["nlp/news/cooperativa"],"dSet":["sup300ch"],"model-vec":["TFIDFWB"],\
#        "model":["LSA"],"mParam":["svd100"],"vParam":["nw5000"]}
#===============================================================================

jIn = {"txt":["Hola Mundo"],"dLake":["nlp/news/cooperativa"],"dSet":["sup300ch"],"model-vec":["TFIDFWB"],\
       "model":["LSA"],"mParam":["svd100"],"vParam":["nw5000"]}

#===============================================================================
# 
# inTxt = jIn["txt"][0]
# dLake = jIn["dLake"][0]
# dSet = jIn["dSet"][0]
# model = jIn["model"][0]
# mParam = jIn["mParam"][0]
# modelVec = jIn["model-vec"][0]
# vParam = jIn["vParam"][0]
# nReg = 5 if "nReg" not in jIn.keys() else int(jIn["nReg"][0])
#===============================================================================


#===============================================================================
# task = app.send_task("add",args=[2,3])
# while True:
#     print("Esperando respuesta....")
#     time.sleep(1)
#     if task.ready():
#         print(task.get())
#         os.sys.exit()
#===============================================================================


#===============================================================================
# task = app.send_task("nlp_news_cooperativa_sup300ch_TFIDFWB",args=[jIn])
# while True:
#     print("Esperando respuesta....")
#     time.sleep(1)
#     if task.ready():
#         print(task.get())
#         os.sys.exit()
#===============================================================================


#===============================================================================
# task = app.send_task("process",args=["FUNC...",jIn])
# while True:
#     print("Esperando respuesta....")
#     time.sleep(1)
#     if task.ready():
#         print(task.get())
#         os.sys.exit()
#===============================================================================
        
        
        
        
#===============================================================================
# def add(func):
#     rr = range(0,20)
#     tasks = [app.send_task(func, args=[i, 5]) for i in rr]
#     print("enviadas....")
#     rep = {}
#     while True:
#         for i in rr:
#             if tasks[i].ready():
#                 r = tasks[i].get()
#                 print(r)
#                 rep[r[0]] = r[1]
#         ll = list(map(lambda x: x.ready(),tasks))
#         print(ll)
#         if list(filter(lambda x: not x, ll ))==[]:
#             break
#         time.sleep(1)
#     return rep
# 
# r1=add("add")
# r2=add("add2")
# 
# print(r1)
# print(r2)
# #from celery.task.http import URL
# #res = URL('http://example.com/multiply').get_async(x=10, y=10)
# #print(res)
#===============================================================================
