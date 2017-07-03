# coding: utf-8

from dpparser import Parser


html = u'''
<!--html网页源代码-->
<html>
    <div>
        <p class='content'>大家好!</p>
        <p class='content'>这里是猿来如此。。。</p>
        <p class='content'>很高兴在这里认识你。</p>
        <p class='content'>我叫窦朋。</p>
        <p class='content'>是python爱好者。</p>
    </div>
    <div>
        <span>电话: 1234567</span>
        <span>金额: 100.12元</span>
    </div>
</html>
'''

# 这里的 html 就模拟的是 requests 库请求的 response.text

data = Parser(data=html, url='http://www.xxx.com')

p_all = data.xpathall('//p')
p_one = data.xpathone('//p')
p_all2 = data.reall('<p.*?p>')
p_one2 = data.reone('<p.*?p>')

# [<dpparser.Parser object at 0x0000000002AE74E0>, ... , <dpparser.Parser object at 0x0000000002AE7550>]
#  <dpparser.Parser object at 0x0000000002AE75C0>
# [<dpparser.Parser object at 0x0000000002AE743D>, ... , <dpparser.Parser object at 0x0000000002AE7C43>]
#  <dpparser.Parser object at 0x0000000002AE75R5>

print p_all[0].unicode()
print p_all[1].unicode()
print p_one.unicode()
print p_all2[0].unicode()
print p_all2[1].unicode()
print p_one2.unicode()

# 大家好!
# 这里是猿来如此。。。
# 大家好!


p2 = data.xpathone('//p[2]').resub(u'。',u'!').bytes()
p5 = data.xpathone('//p[5]').reone(u'是(\w+)').bytes()
print p2
print p5

# 这里是猿来如此！！！
# python

phone = data.xpathone('//span[1]').reone('(\d+)').int()
money = data.xpathone('//span[2]').reone('(\d+\.\d+)').float()
print phone
print money

# 1234567
# 100.12

html = u'''
    <!--html网页源代码-->
        <div>
           <p class='content'>发布于：59秒前 作者:窦朋</p>
           <p class='content'>发布于：23分钟前 作者:窦朋</p>
           <p class='content'>发布于：13小时前 作者:窦朋</p>
           <p class='content'>发布于：5天前 作者:窦朋</p>
           <p class='content'>发布于：2周前 作者:窦朋</p>
           <p class='content'>发布于：今天10:12 作者:窦朋</p>
           <p class='content'>作者:窦朋 发布于：昨天 02:21:45</p>
           <p class='content'>作者:窦朋 发布于：前天12:21</p>
           <p class='content'>作者:窦朋 发布于：2015年6月23日 12:45</p>
           <p class='content'>作者:窦朋 发布于：2015-07-24 16:05:21</p>
           <p class='content'>作者:窦朋 发布于：2017/01/14 13:04</p>
        </div>
'''

data = Parser(data=html)
p_all = data.xpathall("//p")
for p in p_all:
    print p.datetime()

# 2017-02-03 10:54:50
# 2017-02-03 10:32:49
# 2017-02-02 21:55:49
# 2017-01-29 10:55:49
# 2017-01-20 10:55:49
# 2017-02-03 10:12:00
# 2017-02-02 02:21:45
# 2017-02-01 12:21:00
# 2015-06-23 12:45:00
# 2015-07-24 16:05:21
# 2017-01-14 13:04:00

# datetime(timeStrFormat="%Y-%m-%d %H:%M:%S",returnStrType=True)
# 默认的时间格式为 %Y-%m-%d %H:%M:%S
# 默认返回的时间类型是 string
# 如果将 returnStrType 设置为 False,则返回 datetime.datetime 的时间格式

time1 = data.xpathone('//p[1]').datetime("%B,%d,%Y")
time2 = data.xpathone('//p[2]').datetime()
time3 = data.xpathone('//p[2]').datetime(returnStrType=False)
print time1
print time2, type(time2)
print time3, type(time3)

# February,03,2017
# 2017-02-03 10:44:57 <type 'str'>
# 2017-02-03 10:44:57 <type 'datetime.datetime'>

