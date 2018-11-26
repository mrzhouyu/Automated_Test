# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 16:09
# @Author  : YuChou
# @Site    :
# @File    : TryConPi.py
# @Software: PyCharm
from pexpect.pxssh import pxssh
import pexpect
import time
import re
PORT=22
HOST="10.230.0.41"
USER="zhouy"
PWD="Zhouy123!"

class API():
    def __init__(self,host=HOST,user=USER,pwd=PWD,port=PORT):
        self.host=host
        self.user=user
        self.pwd=pwd
        self.port=port

    def conPish(self):
        print("连接pish")
        console = pexpect.spawn("ssh {}@{} -p {}".format(self.user,self.host,self.port))
        #第一次可能链接不上 开启此语句
        # if console.expect("yes/no",timeout=5):
        #     console.sendline("yes")
        console.expect('password')
        console.sendline("Zhouy123!")
        console.expect(["$",pexpect.EOF])
        console.sendline('pish')
        console.expect([">",pexpect.EOF])
        return console

    def listDevices(self,times):
        #指定过滤ID
        id_list=input("Usage:id1,id2,id3,...  : ").split(',')
        con=self.conPish()
        n=0
        while True:
            n+=1
            con.sendline("listDevices")
            con.expect("Total",timeout=3)
            print('获取信息成功：')
            datas=con.before.decode().split('\r\n')
            #print(len(datas))
			#str=''
			#for i,data in enumerate(datas):
			#	str+=data
				#print(i,end='')
				#打印信息开关
				#print(data)
			#if 'offline' in str:
			#	print("有设备掉线")
			#	with open("offline.txt",'a') as f:
			#		f.write("有设备掉线:"+time.asctime(time.localtime())+'\n')
			#else:
			#	with open("offline.txt",'a') as f:
            #		f.write("没有设备掉线:"+time.asctime(time.localtime())+'\n')
            offline_list=[]
            for j in datas:
                for id in id_list:
                    id=' '+id+' '
                    if id in j:
                        status=re.findall(r'(offline|online)',j)[0]
                        if status=='offline':
                            offline_list.append(id.strip())
                            with open("Error.log",'a') as f:
                                f.write("id 为 {}设备掉线！时间是:{}".format(id.strip(),time.asctime(time.localtime()))+'\n')

                    else:
                        continue
            if len(offline_list)==0:
                print("设备状态良好！")
            else:
                print("下列设备有掉线：")
                print(offline_list)
            if n > times:
                break
            time.sleep(300)
		
    def help(self):
        con=self.conPish()
        con.sendline("help")
        con.expect("setSkuPosition",timeout=3)
        print('如下字符串来自远程主机：')
        datas=con.before.decode().split('\r\n')
        for i,data in enumerate(datas):
            print(data)


    def writeLog(self,str):
        with open('log.txt',"a") as f:
            f.write(str+'current time:'+time.asctime(time.localtime())+'\n')

    def ota_GWSL(self):
        con=self.conPish()
        cmd1="http://10.230.0.49/ota/SRSP01/SmartRetail-295-20180814-160919/ota/SR-GWSL-M527-A000-FN3-H030-V1.0.109.ota "
        expect_str1="current version: 1.0.113, new version: 1.0.109"
        cmd2="http://10.230.0.49/ota/SRSP01/SmartRetail-301-20180815-155414/ota/SR-GWSL-M527-A000-FN3-H030-V1.0.113.ota "
        expect_str2 = "current version: 1.0.109, new version: 1.0.113"
        con.sendline('queryDeviceInfo id 61')
        con.expect([' Type Name          GWSL'],timeout=3)
        datas=con.before.decode().split('\n\r')
        print("datas长度"+str(len(datas)))
        print("end"+datas[-1])

        if "Device Sn          d88039a31c35" not in datas[-1]:
            print("该设备掉线了")
            self.writeLog("该设备不在线")
            exit(1)
        elif "Firmware Version   1.0.113" in datas[-1]:
            print("send order 1")
            con.sendline(cmd1)
            time.sleep(250)
            try:
                con.expect(expect_str1,pexpect.EOF)
                print("升级109版本成功")
                self.writeLog("升级109版本成功")
            except:
                print("升级失败")
                self.writeLog("升级失败")
        elif "Firmware Version   1.0.109" in datas[-1]:
            print('send order 2')
            con.sendline(cmd2)
            time.sleep(250)
            try:
                con.expect(expect_str2)
                print("升级109版本成功")
                self.writeLog("升级113版本成功")
            except:
                print("升级错误")
                self.writeLog("升级错误")

        else:
            print("遇到未知错误")
            self.writeLog("遇到未知错误")
            exit(1)
    def ota_GCDSC(self):
        pass

    def ConfSkuPosition(self):
        pass

    def InfoGwsl(self):
        pass
    def InfoCdsc(self):
        pass


if __name__=="__main__":
    INS=API(host="10.230.0.41",user="zhouy",pwd="Zhouy123!",port=22)
#    cur=INS.main()
    times=int(input("持续循环次数："))
    INS.listDevices(times=times)
    # INS.help()
    #INS.ota_GWSL()
