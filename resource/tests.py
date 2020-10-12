from django.test import TestCase

# Create your tests here.
# from aixxuser.methods import *
#
#
# print(md5("aa"))


from aixxuser.tasks import sum


print(sum(3,4))