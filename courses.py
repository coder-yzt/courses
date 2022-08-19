import requests
import json
import datetime
from requests.exceptions import *

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
    {"weekday":"Tuesday",
    "courses": [
        {
            "course_name": course_const["sfs"],
            "time": time_const["one"],
            "week": week_const[1:15],
            "place": "2501"
        },{
            "course_name": course_const["fxff"],
            "time": time_const["three"],
            "week": week_const[1:15],
            "place":"6阶梯"
        }
    ]
    },{"weekday":"Wednesday",
    "courses": [
        {
            "course_name": course_const["fxff"],
            "time": time_const["three"],
            "week": week_const[1:15],
            "place": "6阶梯"
        }
    ]
    },{"weekday":"Thursday",
    "courses": [
        {
            "course_name": course_const["sfy"],
            "time": time_const["one"],
            "week": week_const[3:16],
            "place": "2501"
        },{
            "course_name": course_const["sfs"],
            "time": time_const["three"],
            "week": week_const[1:15],
            "place":"2501"
        }
    ]
    },{"weekday":"Friday",
    "courses": [
        {
            "course_name": course_const["sfy"],
            "time": time_const["one"],
            "week": week_const[3:16],
            "place": "2501"
        },{
            "course_name": course_const["sfs"],
            "time": time_const["three"],
            "week": week_const[1:15],
            "place":"2501"
        }
    ]
    },{"weekday":"Sunday",
    "courses": [
        {
            "course_name": course_const["sfs"],
            "time": time_const["one"],
            "week": [week_const[2],week_const[7]],
            "place": "2504"
        },{
            "course_name": course_const["sfy"],
            "time": time_const["one"],
            "week": [week_const[3],week_const[4],week_const[5],week_const[8],week_const[9],week_const[10],week_const[13],week_const[14],week_const[15]],
            "place":"2406"
        },{
            "course_name": course_const["sfs"],
            "time": time_const["three"],
            "week": [week_const[4],week_const[5],week_const[9],week_const[10]],
            "place": "2501"
        },{
            "course_name": course_const["sfy"],
            "time": time_const["three"],
            "week": [week_const[6],week_const[7],week_const[11],week_const[12],week_const[14]],
            "place": "2104"
        }
    ]
    }
]

# 计算今天是第几周
def get_current_week(open_time):
    open_time = datetime.datetime.strptime(open_time,"%y/%m/%d")
    today_time = datetime.datetime.today()
    # today_time = datetime.datetime.strptime(today,"%y/%m/%d")
    return (today_time - open_time).days // 7 + 1 

# 计算今天是周几
def get_today_time():
    today = datetime.date.today()
    return weekday_const[today.weekday()]

# 拿到今天的课程列表
def get_today_course_list(weekday,current_week):
    # 拿到今天的课表
    today = None
    for i in course_list:
        if weekday == i["weekday"]:
            today = i
    courses = today["courses"]
    
    # 根据今天的周数筛选出是否今天需要上课
    m_courses = []
    for course in courses:
        if current_week in course['week']:
            m_courses.append(course)
    today["courses"] = m_courses
    return today

# 将课程列表格式化，变成推送的格式
def format_course_list(current_week,today_courses):
    today = datetime.datetime.today()
    result1 = "### 今天是{}月{}号，第{}周，星期{}\n\n".format(today.month,today.day,current_week,today.weekday()+1)
    if today_courses["courses"] == []:
        return result1+"今天没有课！"
    result2 = "### 今天的课有：\n\n-----------------------------------\n\n"
    courses = today_courses['courses']
    result3 = ""
    for course in courses:
        result3 += course["course_name"]
        result3 += "\n"
        result3 += "{}节\n".format(course["time"])
        result3 += "地点：{}".format(course["place"])
        result3 += "\n\n-----------------------------------"
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
    sckey = 'SCT145803TAlKgazcPaNkOrwRijZBNEOJ6'
    # What weekday today is
    today = "22/08/30"
    # weekday = get_today_time()
    weekday = weekday_const[datetime.datetime.strptime(today,"%y/%m/%d").weekday()]
    # open school time
    open_time = "22/08/29"
    # get current count of week
    current_week = get_current_week(open_time)
    # print(current_week)
    # get today's courses list
    today_courses = get_today_course_list(weekday,current_week)
    # print(today_courses)
    # format the courses list
    # today_courses = {"courses":[{"course_name":"数学分析","time":"1,2","place":"2501"},{"course_name":"高等代数","time":"1,2","place":"2501"}]}

    courses_str = format_course_list(current_week,today_courses)
    short = get_short(today_courses)
    # print(courses_str)
    # print(short)
    notify(sckey=sckey,message=courses_str,short=short)

if __name__ == '__main__':
#   str2 = '_MHYUUID=cd3fd3d8-7396-4c72-8eca-60c4c49bb182; mi18nLang=zh-cn; ltoken=Q0NYaaDaRW5G2A43Lh36xIi6CxH3KVBqxo1xt4VQ; ltuid=313531694; cookie_token=4QthZSBWToRGhgUn8dtdx5qq0zdpcaxdlblKvEIb; account_id=313531694'

#   sckey = 'SCT145803TAlKgazcPaNkOrwRijZBNEOJ6'

#   notify(sckey,"今天的课表是：...")
    main()
