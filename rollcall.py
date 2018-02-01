'''
##

ToDoList
- cookie處理改用session.

##
'''
import requests
import json
import time
from pprint import pprint as pp

url = 'https://irs.zuvio.com.tw/app_v2/'
def login(email,passwd):
	data = dict(email=email,password=passwd)
	r = json.loads(requests.post(url+'login',data=data).text)
	token,user_id = r['accessToken'],r['user_id']
	getCourseList(token,user_id)

def getCourseList(token,user_id):
	data = dict(accessToken=token,user_id=user_id)
	r = json.loads(requests.post(url+'getCourseList',data=data).text)
	for x in r['semesters'][0]['courses']:
		if x['name'] == '綠色行銷管理':
			course_id = x['course_id']
			makeRollcall(token,user_id,course_id)
			break

def makeRollcall(token,user_id,course_id):
	data = dict(accessToken=token,user_id=user_id,course_id=course_id)
	r = json.loads(requests.post(url+'getRollCall',data=data).text)
	rollcall_id = r['rollcall']
	data = dict(accessToken=token,user_id=user_id,rollcall_id=rollcall_id)
	r = requests.post(url+'makeRollcall',data=data)
	if r.json()['status'] != False:
		print('簽到完成')
