import requests
import json
import datetime
from requests.exceptions import *
from dongbaqu import *
from copy import deepcopy

course_const = {
"fxff" : "分析方法",
"sfy" :"数学分析1",
"sfs" : "数学分析3"
}
time_const = {
    "one":"1、2",
    "three":"3、4"
}
weekday_const = ["Monday","Tuesday","Wednesday","Thursday","Friday","Satursday","Sunday"]
week_const = [i for i in range(16)]

course_list = [
    {'weekday': 'Tuesday', 
    'courses': [
        {'course_name': '数学分析3', 'time': '1、2', 'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 'place': '2501'}, 
        {'course_name': '分析方法', 'time': '3、4', 'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 'place': '6阶梯'}
        ]}, 
    {'weekday': 'Wednesday', 
    'courses': [
        {'course_name': '分析方法', 'time': '3、4', 'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 'place': '6阶梯'}
    ]}, 
    {'weekday': 'Thursday', 
    'courses': [
        {'course_name': '数学分析1', 'time': '1、2', 'week': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'place': '2501'}, 
        {'course_name': '数学分析3', 'time': '3、4', 'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 'place': '2501'}
        ]}, 
    {'weekday': 'Friday', 
    'courses': [
        {'course_name': '数学分析1', 'time': '1、2', 'week': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'place': '2501'}, 
        {'course_name': '数学分析3', 'time': '3、4', 'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 'place': '2501'}
    ]}, 
    {'weekday': 'Sunday', 
    'courses': [
        {'course_name': '数学分析3', 'time': '1、2', 'week': [2, 7], 'place': '2504'}, 
        {'course_name': '数学分析1', 'time': '1、2', 'week': [3, 4, 5, 8, 9, 10, 13, 14, 15], 'place': '2406'}, 
        {'course_name': '数学分析3', 'time': '3、4', 'week': [4, 5, 9, 10], 'place': '2501'}, 
        {'course_name': '数学分析1', 'time': '3、4', 'week': [6, 7, 11, 12, 14], 'place': '2104'}
    ]}
]

# 计算今天是第几周
def get_current_week(open_time,now_time):
    open_time = datetime.datetime.strptime(open_time,"%y/%m/%d")
    today_time = datetime.datetime.strptime(now_time,"%y/%m/%d")
    # today_time = datetime.datetime.strptime(today,"%y/%m/%d")
    return (today_time - open_time).days // 7 + 1 

# 计算今天是周几
def get_today_time(now_time):
    today = datetime.datetime.strptime(now_time,"%y/%m/%d")
    return weekday_const[today.weekday()]

# 拿到今天的课程列表
def get_today_course_list(weekday,current_week):
    # 拿到今天的课表
    ##################################################################
    # today = {"courses":[]}
    # for i in course_list:
    #     if weekday == "Sunday" and i['weekday'] == "Sunday":
    #         print(i)
    #     if weekday == i["weekday"]:
    #         today = i
    #     courses = today["courses"]
    #################################################################
    today = deepcopy([i for i in course_list if i["weekday"] == weekday])
    
    if len(today) == 1:
        today = today[0]
    else:
        return {"courses":[]}
    # print(today["courses"] if today["weekday"] == "Sunday" else "")
    with open("aaa.txt",'a') as f:
        f.write(str(today))

    courses = today["courses"]
    # 根据今天的周数筛选出是否今天需要上课
    m_courses = []
    for course in courses:
        if current_week in course['week']:
            m_courses.append(course)
    today["courses"] = m_courses
    
    return today

# 将课程列表格式化，变成推送的格式
def format_course_list(now_time,current_week,today_courses):
    today = datetime.datetime.strptime(now_time,"%y/%m/%d")
    w = ['','一','二','三','四','五','六','日']
    result1 = "\n\n### 今天是{}月{}号，第{}周，星期{}\n\n".format(today.month,today.day,current_week,w[today.weekday()+1])
    if today_courses["courses"] == []:
        return result1+"-----------------------------------\n\n今天没有课！\n\n"
    result2 = "今天的课有：\n\n-----------------------------------\n\n"
    courses = today_courses['courses']
    result3 = ""
    for course in courses:
        result3 += course["course_name"]
        result3 += "\n\n"
        result3 += "{}节\n\n".format(course["time"])
        result3 += "周次:{}\n\n".format(course["week"])
        result3 += "地点：{}".format(course["place"])
        result3 += "\n\n-----------------------------------\n\n"
    return result1 + result2 + result3


def get_short(today_courses):
    courses = today_courses["courses"]
    c = []
    for course in courses:
        c.append(course["course_name"])
    return " ".join(c)


def notify(sckey, message,short):
  if sckey.startswith('SC'):
    print('准备推送通知...')
    url = 'https://sc.ftqq.com/{}.send'.format(sckey)
    data = {'text': '课表推送通知', 'desp': message,"short":short}
    try:
      jdict = json.loads(
              requests.Session().post(url, data = data).text)
    except Exception as e:
      print(e)
      raise HTTPError
    else:
      try:
        errmsg = jdict['errmsg']
        if errmsg == 'success':
          print('推送成功')
        else:
          print('{}: {}'.format('推送失败', jdict))
      except:
        print('推送失败')
  else:
    print('未配置SCKEY,正在跳过推送')

  return print('任务结束')


def main():
    sckey1 = 'SCT145803TAlKgazcPaNkOrwRijZBNEOJ6'
    sckey2 = 'SCT166909TzrwgD9pvfzDNdcm0UAhpzHKk'
    # What weekday today is
    # today = "22/08/30"
    
    utc_now = datetime.datetime.utcnow()
    convert_now = TimeUtil.convert_timezone(utc_now, '+8')
    today = str(convert_now.year)[2:] + '/' + str(convert_now.month) + '/' + str(convert_now.day)
    # weekday = get_today_time()
    weekday = weekday_const[datetime.datetime.strptime(today,"%y/%m/%d").weekday()]
    # open school time
    open_time = "22/08/29"
    # get current count of week
    current_week = get_current_week(open_time,today)
    # print(current_week)
    # get today's courses list
    today_courses = get_today_course_list(weekday,current_week)
    # print(today_courses)
    # format the courses list
    courses_str = format_course_list(today,current_week,today_courses)
    short = get_short(today_courses)
    # print(course_list)
    print(courses_str)
    # print(short)
    notify(sckey=sckey1,message=courses_str,short=short)
    notify(sckey=sckey2,message=courses_str,short=short)
        

if __name__ == '__main__':
#   sckey = 'SCT145803TAlKgazcPaNkOrwRijZBNEOJ6'
    main()
    # with open("aaa.txt",'w')as f:
    #     f.write(str(course_list))
