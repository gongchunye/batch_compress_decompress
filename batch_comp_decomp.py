# Author: Chunye Gong，NUDT
# Time：  20210505 V1
# 批量文件加解密，主要对一些个人文件加个密
# 省去手动用加解密输入密码的过程，目前还不完备，智能化程度不高
# 依赖：装好7z软件和Python 3
# 使用说明：
# 1）line 1，修改可执行文件7z.exe路径
# 2）line 2, comp or decomp
# 3）line 3, 是否删除压缩或者解压的源文件
# 4）line 4, 可以修改密码，
# 5）line 5, 7z(能够加密文件名) or zip
import os,sys


class COMPDECOMP():
    exe=r'"C:\Program Files\7-Zip\7z.exe" '

    # 可以修改密码，但是一定要记得。因为只是批量处理一下，所以建议改成常用密码。
    passwd="123456"
    beCompress=True
    beDeleteSource=True

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
    #     这个表示直接覆盖现有文件，而没有任何提示。类似的参数还有：
    #     -aos 跳过现有文件，其不会被覆盖。
    #     -aou 如果相同文件名的文件以存在，将自动重命名被释放的文件。举个例子，文件 file.txt 将被自动重命名为 file_1.txt。 
    #     -aot 如果相同文件名的文件以存在，将自动重命名现有的文件。举个例子，文件 file.txt 将被自动重命名为 file_1.txt。

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

        filetype=os.path.splitext(input1)[-1]
        bExist=False
        if filetype=='7z' or filetype=='zip':
            if(not os.path.isfile(input1)):
                print("Error1234: decompressIT, no such file --",input1)
                return
                
        if ( os.path.isfile(input1+".zip")):
            bExist=True
            input1=input1+".zip"
        if (os.path.isfile(input1+".7z") ):
            bExist=True
            input1=input1+".7z"
        if not bExist:
            print("Error1235: decompressIT, no such file --",input1+" .zip or .7z")
            return

        ss=input1.split("\\")
        dir1=''
        for i in range(len(ss)-1):
            dir1=dir1+ss[i]+'/'
        # print(dir1)
        os.chdir(dir1)

        cmd=self.exe+" x "+input1+self.decomp_parameters+ " -p"+self.passwd
        print(cmd)
        result = os.popen(cmd).read()
        # print(result)
        if ("Everything is Ok" in result):
            if self.beDeleteSource:
                os.remove(input1)
                print("delete "+input1)
            print("Good. Decompress is Ok.")

    # compressIT(passwd,inputx1)
    # decompressIT(passwd, inputx2)


    def getConfig(self):
        fi=open(self.configfile)
        fl=fi.readlines()
        fi.close()
        ss=fl[0].strip().split("###exe=")
        self.exe='"'+ss[1]+'"'

        ss=fl[1].strip().split("###compress_or_decompress=")
        if (ss[1]=="comp"):
            self.beCompress=True
        if (ss[1]=="decomp"):
            self.beCompress=False

        ss=fl[2].strip().split("###deleteSourceFile=")
        if int(ss[1])==1:
            self.beDeleteSource=True
        if int(ss[1])==0:
            self.beDeleteSource=False
            
        ss=fl[3].strip().split("###password=")
        self.passwd=ss[1]

        ss=fl[4].strip().split("###type=")
        self.itype=ss[1]

        print(self.exe)
        print(self.beCompress)
        print(self.beDeleteSource)
        print(self.passwd)
        print(self.itype)

        
        self.comp_parameters=self.comp_parameters+" -p"+self.passwd +" -t"+self.itype+" "

        if self.itype=="7z":
            self.comp_parameters=self.comp_parameters+' -mhe '
        if self.beDeleteSource:
            self.comp_parameters=self.comp_parameters+' -sdel '

        fileList=list()
        for i in range(5,len(fl)):
            ss=fl[i].strip()
            fileList.append(ss)
        return fileList

    def runIT(self):
        objList=self.getConfig()
        for inp in objList:
            if self.beCompress:
                self.compressIT(inp)
            else:
                self.decompressIT(inp)
        

obj=COMPDECOMP()
obj.runIT()


