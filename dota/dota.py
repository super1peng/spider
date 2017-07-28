#coding:utf-8

# 抓取dota基本内容
# 爬虫路线: requests -bs4
# Python 版本: 2.7
# OS: mac os

#------------------编码--------------
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#------------------------------------

import requests
import bs4 


#---------------抓取网页到本地的代码框架------------
def get_html(url):
	try:
		r = requests.get(url, timeout=30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		#r.encoding = 'utf-8'
		return r.text

	except:
		return "ERROR "

def print_result(url):
	# 查询比赛结果，并格式化输出！

	html = get_html(url)
	soup =  bs4.BeautifulSoup(html,'lxml')
	match_list = soup.find_all('div', attrs={'class': 'matchmain bisai_qukuai'})
	for match in match_list:
		time = match.find('div', attrs={'class': 'whenm'}).text.strip()
		teamname = match.find_all('span', attrs={'class': 'team_name'})

		# 由于网站的构造问题，队名有时候会不显示，所以我们需要过滤一些注释：方法如下

		if teamname[0].string[0:3] == 'php':
			team1_name = "暂无队名"
		else:
			team1_name = teamname[0].string

		# 这里我们采用css选择器：比原来的属性选择方法更加的方便
		team1_support_level = match.find('span', class_='team_number_green').string

		team2_name = teamname[1].string
		team2_support_level = match.find('span', class_='team_number_red').string
		print('比赛时间：{}，\n 队伍一：{}      胜率 {}\n 队伍二：{}      胜率 {} \n'.format(time,team1_name,team1_support_level,team2_name,team2_support_level))




def main():
	url = 'http://dota2bocai.com/match'
	print_result(url)

if __name__== '__main__':
	main()
