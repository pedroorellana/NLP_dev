#!/usr/bin/python
# encoding: utf-8
"""
Created on 2018-06-22
@author: tmardesic
"""
import os,sys,time,stat
from tsmUtil_py import *


# Help
if len(sys.argv)==1:
    print "\n   *** target-IP-USR-PASSWD  [MODULES] ***"
    print "   w-base  w-js  w-html w-images w-all"\
    +"\n   ai-base ai-nlp-classifyer  ai-nlp-relationships"\
    +"\n   util : locale :  \n"
    os.sys.exit()


ip = "10.20.0.114"
usr = "root"
port=22
passwd = "tec1465"
#-------------------------------------------------------------------------
if str(sys.argv)>1:
    if sys.argv[1].startswith("target-"):
        target = sys.argv[1].split("-")
        if not (len(target))>=4:
            print str(target)+"  target Error !! \n  Example:  target-10.20.0.160-root-gprs06"
            os.sys.exit()
        ip = target[1]
        usr = target[2]
        passwd = target[3]
        try:
            port = int(target[4])
        except:
            port = 22
        del sys.argv[0]



ver = "1.0"
server = {"ip":ip,"user":usr,"password":passwd,"port":port}

path = os.path.dirname(os.path.abspath(__file__))


print "Install --- "+ip +"  -- "+path
#"/Users/tmardesic/eclipse_new/tsmVCS_py/vcs-server-py-"+ver

#LIB_DIR = "/Users/tmardesic/eclipse_new/tsmLibrary"
#-------------------------------------------------------------------------
ssh= Ssh(server["ip"], server["user"], server["password"], server["port"])

mods = sys.argv[1:]


# Si enceuntro args que parten con w- , agrego modulo webserver
#for m in mods:
#    if m.startswith("w-"):
#        mods+["webserver"]
        
   

# Copia modulos
for m in mods:
    
    if m in ["locale","supervisor","base","tsmutil"]:
        continue

    if m.startswith("w-all"):
        ssh.cmd("mkdir /opt/tsmAI/Web")

    if m=="w-all":
        ssh.put(path+"/Web/_NLPChatbot", "/opt/tsmAI/Web")
        ssh.put(path+"/Web/_NLPClassifyer", "/opt/tsmAI/Web")
        ssh.put(path+"/Web/_NLPRelationships", "/opt/tsmAI/Web")
        ssh.put(path+"/Web/_NLPVectorizer", "/opt/tsmAI/Web")
        ssh.put(path+"/Web/cert", "/opt/tsmAI/Web")
            
        ssh.put(path+"/Web/modHttpServer", "/opt/tsmAI/Web")
        ssh.put(path+"/Web/modJwt", "/opt/tsmAI/Web")
        ssh.put(path+"/Web/modLog", "/opt/tsmAI/Web")
        ssh.put(path+"/Web/modMonitor", "/opt/tsmAI/Web")
        ssh.put(path+"/Web/modWeb", "/opt/tsmAI/Web")
        ssh.put(path+"/Web/util", "/opt/tsmAI/Web")        
        ssh.put(path+"/Web/conf.txt", "/opt/tsmAI/Web/conf.txt")
        ssh.put(path+"/Web/README.md", "/opt/tsmAI/Web/README.md")
        ssh.put(path+"/Web/tsmaiweb.py", "/opt/tsmAI/Web/tsmaiweb.py")
        
    if m=="w-base":
        ssh.put(path+"/Web/tsmaiweb.py", "/opt/tsmAI/Web/tsmaiweb.py")
    
    if  m=="ai-base":
        ssh.put(path+"/Log.py", "/opt/tsmAI/Log.py")
        ssh.put(path+"/Config.py", "/opt/tsmAI/Config.py")
        ssh.put(path+"/config.txt", "/opt/tsmAI/config.txt")
        ssh.put(path+"/GlobalContext.py", "/opt/tsmAI/GlobalContext.py")
        ssh.put(path+"/tsmai.py", "/opt/tsmAI/tsmai.py")
        ssh.put(path+"/BaseEtl.py", "/opt/tsmAI/BaseEtl.py")


# locale
if "locale" in mods:
    print ssh.cmd("echo -e 'LC_ALL=\"en_US.UTF-8\"\nLANG=\"en_US.UTF-8\"\nLANGUAGE=\"en_US.UTF-8\"' > /etc/environment")
    print ssh.cmd("(echo \"with open('/etc/locale.gen') as file: ar= [l.replace('\\n','') for l in file.readlines()]\" ; echo \"for l in ar:\" ; echo \"    if  l.find('en_US.UTF-8')>=0:\"; echo \"        print 'en_US.UTF-8 UTF-8'\" ; echo \"    else:\" ; echo \"        print l\") | python > /etc/locale.gen.tmp")
    print ssh.cmd("cat /etc/locale.gen.tmp > /etc/locale.gen; rm -f /etc/locale.gen.tmp")
    print ssh.cmd("locale-gen en_US.UTF-8; update-locale en_US.UTF-8")

# 
if "tsmutil" in map(lambda x: x.lower(),mods):
    
    #LIB_DIR = "/Users/tmardesic/eclipse_new/tsmLibrary/tsm_py/tsm-util-py"
    
    LIB_DIR = "/opt/eclipse/tsmLibrary/"
    #"/Users/tmardesic/eclipse_new/tsmLibrary/"
    ret= ssh.cmd("mkdir /opt/INSTALL ; rm -f -R /opt/INSTALL/tsm-util-py")
    ssh.put(LIB_DIR+"/tsm_py/tsm-util-py", "/opt/INSTALL")
    ret= ssh.cmd("cd /opt/INSTALL/tsm-util-py ;  python setup.py bdist_egg")
    time.sleep(5)
    print "--------------\n"+ret
    ret= ssh.cmd("cd /opt/INSTALL/tsm-util-py ;  python setup.py install")
    print "\n--------------\n"+ret
    os.sys.exit()



# ===== MAIN ===================
#install(host,port,user,password)

""" 
ssh.cmd("mkdir /etc/vcs ; mkdir /var/log/vcs ; mkdir /opt/vcs-server-py-"+ver)
ssh.put(path+"/etc/vcs-server-py.conf", "/etc/vcs/vcs-server-py.conf")
#ssh.cmd('cat /etc/vcs/vcs-server-py.conf| sed -e s/"vcs00"/"vcs00ctr"/g > /etc/vcs/vcs-server-py.conf.new')
#ssh.cmd("mv  /etc/vcs/vcs-server-py.conf.new  /etc/vcs/vcs-server-py.conf")
ssh.put(path+"/util", "/opt/vcs-server-py")
ssh.put(path+"/images","/opt/vcs-server-py")
# Remve services
cmd ="update-rc.d -f named remove ; update-rc.d -f apache2 remove ; "
cmd+="update-rc.d -f sendmail remove ; update-rc.d -f saslauthd remove ; "
cmd+="apt-get remove rsyslog -y;"
cmd+="cat /etc/inittab | sed s/#l6:6:/l6:6:/g | sed s/l6:6:/#l6:6:/g  "
cmd+="| sed s/#6:23:respawn:/6:23:respawn:/g | sed s/6:23:respawn:/#6:23:respawn:/g "
cmd+="| sed s/#5:23:respawn:/5:23:respawn:/g | sed s/5:23:respawn:/#5:23:respawn:/g "
cmd+="| sed s/#4:23:respawn:/4:23:respawn:/g | sed s/4:23:respawn:/#4:23:respawn:/g "
cmd+=">  /etc/inittab.tmp ; mv  /etc/inittab.tmp  /etc/inittab"
ssh.cmd(cmd)
"""







# sshdCheckUseDNS
"""
ret = ssh.cmd("cat /etc/ssh/sshd_config | grep 'UseDNS no' | wc -l")
ret = " "+ret
print "["+str(ret.replace("\n","").replace("\r","").find("0"))+"]"
if ret.replace("\n","").replace("\r","").find("0")>0:
    print " UseDNS no:   No configuracio. Se realiza configuración ok."
    ssh.cmd("echo 'UseDNS no' >> /etc/ssh/sshd_config")
else:
    print " UseDNS no:   Configuracion ok."
print "--"  
"""

# Supervisor daemon
"""
ssh.cmd("mkdir /etc/supervisor; mkdir /etc/supervisor/conf.d;")
ssh.put(path+"/etc/supervisord.conf", "/etc")
ssh.put(path+"/etc/supervisor/supervisord.sh", "/etc/init.d/")
ssh.cmd("chmod 777 /etc/init.d/supervisord.sh")
ssh.cmd("chmod +x /etc/init.d/supervisord.sh")
ssh.cmd("update-rc.d supervisord.sh defaults")
""" 

# lost+found
"""
ssh.cmd("echo \"alias ls='ls --ignore=lost+found'\" > /root/.bashrc")
"""
