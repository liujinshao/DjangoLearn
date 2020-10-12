import hashlib


def md5(str):
    # 创建md5对象
    str=str.encode('utf-8')
    m = hashlib.md5()
    m.update(str)  # 传入需要加密的字符串进行MD5加密
    return m.hexdigest()  #获取到经过MD5加密的字符串并返回

# bb = md5Encode(aa.encode('utf-8')) # 必须先进行转码，否则会报错
# print(md5Encode("aa"))

