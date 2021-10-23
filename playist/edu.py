import requests

import re

low=0

mid=0

high=0

critical=0

name=''

percent=0.0

#定义漏洞类型和数量

bugsName=['SQL注入漏洞','文件上传漏洞','代码执行漏洞','命令执行漏洞','XSS漏洞','CSRF漏洞','SSRF漏洞','点击劫持漏洞','弱口令','敏感信息泄露','水平权限绕过','垂直权限绕过','其他漏洞']

bugsCount=[0,0,0,0,0,0,0,0,0,0,0,0,0]

#定义漏洞等级和数量

bugsLevel=['低危','中危','高危','严重']

id=input('请输入厂商ID：')

for i in range(1,999):   #此处设置为999为了不用控制页数，使用try进行中断
	userHomeUrl='https://src.sjtu.edu.cn/list/firm/'+id+'?page='+str(i)
	backInfo=requests.get(userHomeUrl)

#print(backInfo.text) #backinfo为响应号，backInfo.text为返回的链接内容。

try:#终止循环
	break_str='?page='+str(i)

#if backInfo.text.find(break_str)==-1:

#print(backInfo.text.find(break_str))

#检查是否包含在指定范围内，如果包含子字符串返回开始的索引值，否则返回-1。

if backInfo.text.find(break_str)==-1 and i!=1:#完成后修改，防止页数不足一页而跳出循环
	print('第'+str(i)+'页，不存在，循环终止！')
	break

#正则规则中保留尖括号为了提高准确率，防止匹配到用户昵称和用户签名

r_name=r'学校名称：.+?<' #输出学校名称：.+?< <h2>学校名称:温州大学</h2>

# 1、. 匹配任意1个字符(除了\n)

# 2、+ 匹配前一个字符出现1次多次或则无限次,直到出现一次

# 3、? 匹配前一个字符出现1次或者0次,要么有1次,要么没有

r_total=r'漏洞总数：\d+' #\d 匹配数字,也就是0-9

r_valid=r'漏洞威胁值：\d+'

r_low=r'>低危<'

r_mid=r'>中危<'

r_high=r'>高危<'

r_critical=r'>严重<'

if name=='':

#print(re.search(r_name,backInfo.text)) #学校名称：温州大学<

	name=re.search(r_name,backInfo.text).group().replace('<','') #学校名称：温州大学<替换掉

	#print(re.search(r_total, backInfo.text))

	total = re.search(r_total, backInfo.text).group().replace('漏洞总数：', '')

	# print(total)

	rank = re.search(r_valid, backInfo.text).group().replace('漏洞威胁值：', '') # 此处采用偷懒式写法，偷懒但有效

	# 计算各类型漏洞个数

	# print(len(bugsName))

for ii in range(len(bugsName)):

	# print(ii)

	# print(re.findall(bugsName[ii], backInfo.text)) #爬出来每个漏洞的个数

	bugsCount[ii] = len(re.findall(bugsName[ii], backInfo.text)) + bugsCount[ii]

	# print(bugsCount[ii])

	low_result = re.findall(r_low, backInfo.text) # 低危

	mid_result = re.findall(r_mid, backInfo.text) # 中危

	high_result = re.findall(r_high, backInfo.text) # 高危

	critical_result = re.findall(r_critical, backInfo.text) # 严重

	# 开始计算总通过率

	# print(total)

if percent == 0.0:

	percent = '%.4f' % (float(rank) / float(total))

	# 计算完毕

	# 计算各等级漏洞数

	low = low + len(low_result)

	mid = mid + len(mid_result)

	high = high + len(high_result)

	critical = critical + len(critical_result)

# 状态报告

print('第' + str(i) + '页，已处理！')

except:

	print('出现异常，中断进程')

	break

#打印空行

print('\n')

#bugsName[i]为各种漏洞名

for i in range(len(bugsName)):

	print(bugsName[i]+'：'+str(bugsCount[i]))

	#打印空行
	print('')
	print('计算完毕\n厂商名称：'+name+'\n总漏洞：'+str(total)+'\t总rank：'+str(rank)+'\t平均rank：'+percent+'\n低危：'+str(low)+'\t中危：'+str(mid)+'\t高危：'+str(high)+'\t严重：'+str(critical))