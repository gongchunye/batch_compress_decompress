# batch_compress_decompress

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

运行方式：
python batch_comp_decomp.py
