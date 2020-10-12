from django.test import TestCase

# Create your tests here.
# 导入hash算法库
import hashlib
# 得到md5算法对象
hash_md5 = hashlib.md5()
# 准备要计算md5的数据（bytes类型）
data = 'aaaa'.encode('utf-8', errors='ignore')
# 计算
hash_md5.update(data)
# 获取计算结果(16进制字符串，32位字符)
md5_str = hash_md5.hexdigest()
# 打印结果
print(md5_str)

