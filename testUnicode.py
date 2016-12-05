#coding=utf-8
import sys

s = '谷歌'

type = sys.getfilesystemencoding()
print type
print s.decode('utf-8').encode(type)
print s


print "========="

print unicode(s,'mbcs')



str='我的'
print "string is:"
print str

ustring=u"我的"
print ustring

gbkstring=ustring.encode("mbcs")
print gbkstring

anotherstring=gbkstring.decode("mbcs")
print anotherstring
