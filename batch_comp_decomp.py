# encoding:utf-8

import os,sys

# Author: Chunye Gong，NUDT
# Time：  20210505 V1
# 批量文件加解密，主要对一些个人文件加个密
# 省去手动用加解密输入密码的过程
# 依赖：装好7z软件和Python 3
# 使用说明：
# 1）line 1，修改可执行文件7z.exe路径
# 2）line 2, comp or decomp
# 3）line 3, 是否删除压缩或者解压的源文件
# 4）line 4, 可以修改密码。empty表示密码为空
# 5）line 5, 7z(能够加密文件名) or zip
# 6）line 6, 分卷大小，200m,100k等，小写。-1表示不管大小压缩成单个文件
# 7）line 7, 是否对下一级文件夹进行压缩或者减压缩
# 8）line 8-*，每一行一个加解密文件或者目录

class COMPDECOMP():
    exe=r'"C:\Program Files\7-Zip\7z.exe" '

    # 可以修改密码，但是一定要记得。因为只是批量处理一下，所以建议改成常用密码。
    passwd="empty"
    beCompress=True
    beDeleteSource=True
    bIndir=0

    configfile="config.txt"
    # inputx1=r"C:\Users\anlong\Desktop\tmp\111"
    # inputx2=r"C:\Users\anlong\Desktop\tmp\111.zip"

    # -mx=9，参数表示压缩等级，9级是最高等级。默认等级是5。
    # -mmt=on 这个参数表示开启多线程，提高压缩速度。
    # -sdel 删除掉源文件
    # -mhe  加密文件名
    comp_parameters=" a -r -mx=3 -mmt=on "

    itype="zip"

    # -aoa
    # 这个表示直接覆盖现有文件，而没有任何提示。类似的参数还有：
    # -aos 跳过现有文件，其不会被覆盖。
    # -aou 如果相同文件名的文件以存在，将自动重命名被释放的文件。举个例子，文件 file.txt 将被自动重命名为 file_1.txt。 
    # -aot 如果相同文件名的文件以存在，将自动重命名现有的文件。举个例子，文件 file.txt 将被自动重命名为 file_1.txt。

    decomp_parameters=" -aoa "

    def compressIT(self,input1):
        if(not (os.path.isfile(input1) or os.path.isdir(input1))):
            print("Error1233: compressIT, no such file --",input1)
            return 
        ss=input1.split("\\")
        outname=(ss[len(ss)-1])+"."+self.itype+' '
        dir1=''
        for i in range(len(ss)-1):
            dir1=dir1+ss[i]+'/'
        # print(dir1)
        os.chdir(dir1)


        cmd=self.exe+self.comp_parameters+outname+ input1
        print(cmd)
        result = os.popen(cmd).read()
        # print(result)
        if ("Everything is Ok" in result):
            if self.beDeleteSource:
                print("delete "+input1)
            print("Good. Compress is OK.")        

    def decompressIT(self,input1):

        # filetype=input1.split(".")[-1]
        # print(filetype)
        bExist=False
        # if (filetype=='7z' or filetype=='zip' or filetype=='001') :
        #     if(not os.path.isfile(input1)):
        #         print("Error1234: decompressIT, no such file --",input1)
        #         return
        
        srcList=list()
        del001=input1
        if (os.path.isfile(input1)):
            xx5=input1.split(".")
            xx=xx5[-1]
            if (xx =="zip" or xx=="7z"):
                bExist=True
                srcList.append(input1)

            if xx =='001' and (xx5[-2]=='zip' or xx5[-2]=='7z'):
                bExist=True
                xx1=input1.split(".001")[-2]
                for i in range(1,100000):
                    xx2=xx1+".%03d"%i
                    if os.path.isfile(xx2):
                        srcList.append(xx2)
                    else:
                        break
                    

        if (os.path.isfile(input1+".zip")):
            bExist=True
            input1=input1+".zip"
            srcList.append(input1)
        if (os.path.isfile(input1+".7z")):
            bExist=True
            input1=input1+".7z"
            srcList.append(input1)
        if (os.path.isfile(input1+".7z.001")):
            bExist=True
            for i in range(1,10000):
                xx=input1+".7z.%03d"%i
                if os.path.isfile(xx):
                    srcList.append(xx)
                else:
                    break
            input1=input1+".7z.001"
        if (os.path.isfile(input1+".zip.001")):
            bExist=True
            for i in range(1,10000):
                xx=input1+".zip.%03d"%i
                if os.path.isfile(xx):
                    srcList.append(xx)
                else:
                    break
            input1=input1+".zip.001"
        if not bExist:
            print("Error1235: decompressIT, not compressed file, .zip, .7z, .zip.001, .7z.001\n   ",input1)
            return

        ss=input1.split("\\")
        dir1=''
        for i in range(len(ss)-1):
            dir1=dir1+ss[i]+'/'
        # print(dir1)
        os.chdir(dir1)

        ss=self.decomp_parameters

        if (not self.passwd=="empty"):
            ss=ss+ " -p"+self.passwd

        cmd=self.exe+" x "+input1+" "+ss
        print(cmd)
        result = os.popen(cmd).read()
        # print(result)
        if ("Everything is Ok" in result):
            if self.beDeleteSource:
                # print(srcList)
                for xx in srcList:
                    os.remove(xx)
                print("delete "+input1)
            print("Good. Decompress is Ok.")

    # compressIT(passwd,inputx1)
    # decompressIT(passwd, inputx2)

    def getKeyword(self,xx,key1):
        ss=xx.split(key1)
        return ss[1]

    def getConfig(self):
        fi=open(self.configfile,encoding='utf-8')
        fl=fi.readlines()
        fi.close()

        ss=self.getKeyword(fl[0].strip(),"###exe=")
        self.exe='"'+ss+'"'

        ss=self.getKeyword(fl[1].strip(),"###compress_or_decompress=")
        if (ss=="comp"):
            self.beCompress=True
        if (ss=="decomp"):
            self.beCompress=False

        ss=self.getKeyword(fl[2].strip(),"###deleteSourceFile=")
        if int(ss)==1:
            self.beDeleteSource=True
        if int(ss)==0:
            self.beDeleteSource=False
            
        ss=self.getKeyword(fl[3].strip(),"###password=")
        self.passwd=ss

        ss=self.getKeyword(fl[4].strip(),"###type=")
        self.itype=ss

        ss=self.getKeyword(fl[5].strip(),"###size=")
        self.isize=ss
        
        ss=self.getKeyword(fl[6].strip(),"###indir=")
        self.bIndir=int(ss)
        

        
        self.comp_parameters=self.comp_parameters+ " -t"+self.itype+" "

        if not self.passwd=="empty":
            self.comp_parameters=self.comp_parameters+" -p"+self.passwd + ' '        

        if self.itype=="7z":
            self.comp_parameters=self.comp_parameters+' -mhe '
        if self.beDeleteSource:
            self.comp_parameters=self.comp_parameters+' -sdel '
        if not self.isize=="-1":
            self.comp_parameters=self.comp_parameters+' -v'+self.isize+' '

        fileList=list()
        for i in range(len(fl)):
            if "###" in fl[i]:
                continue
            ss=fl[i].strip()
            # print(ss)
            fileList.append(ss)
        return fileList

    def runIT(self):
        objList=self.getConfig()
        # print(type(objList[0]))
        for inp in objList:
            if self.beCompress:
                if self.bIndir==1 and os.path.isdir(inp):
                    xx1=os.listdir(inp)
                    for xx in xx1:
                        xx2=inp+'\\'+xx
                        self.compressIT(xx2)
                else:
                    self.compressIT(inp)
            else:
                if self.bIndir==1 and os.path.isdir(inp):
                    xx1=os.listdir(inp)
                    for xx in xx1:
                        xx2=inp+'\\'+xx
                        self.decompressIT(xx2)
                else:
                    self.decompressIT(inp)
        

obj=COMPDECOMP()
obj.runIT()


