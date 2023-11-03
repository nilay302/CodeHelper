import json
from django.utils import timezone
import datetime as dt
import requests
import random


def userDetails(codeforcesHandle, clearPastProblems):
    url = requests.get(
        'https://codeforces.com/api/user.info?handles='+codeforcesHandle)
    jsonData = url.json()
    data = json.dumps(jsonData)
    codeforcesHandle = json.loads(data)
    if(codeforcesHandle['status'] != "OK"):
        return False
    if(clearPastProblems):
        completedProblems.clear()
    return codeforcesHandle['result'][0]


def convertUnixTime(unixtime):
    date = dt.datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d')
    time = dt.datetime.fromtimestamp(unixtime).strftime('%H:%M:%S')
    date_time_obj = dt.datetime.strptime(date+" "+time, '%Y-%m-%d %H:%M:%S')
    time = date_time_obj.time()
    time = str((dt.datetime.combine(dt.date(1, 1, 1), time) +
                dt.timedelta(hours=5, minutes=30)).time())
    return date+" "+time


def convertToHour(secondsTime):
    return str(dt.timedelta(seconds=secondsTime))


def contestDetails():
    url = requests.get('https://codeforces.com/api/contest.list')
    jsonData = url.json()
    data = json.dumps(jsonData)
    contests = json.loads(data)
    contestList = []
    count = 0
    for contest in contests['result']:
        if(contest['phase'] == "FINISHED"):
            break
        else:
            contest['startTimeSeconds'] = convertUnixTime(
                contest['startTimeSeconds'])
            contest['durationSeconds'] = convertToHour(
                contest['durationSeconds'])
            contestList.append(contest)
            count += 1
    contestList = contestList[::-1]
    return contestList[0:5]


completedProblems = {}


def getTags(codeforcesHandle, rank):
    url = requests.get(
        'https://codeforces.com/api/user.status?handle='+codeforcesHandle)
    jsonData = url.json()
    data = json.dumps(jsonData)
    submissions = json.loads(data)
    submissions = submissions['result']
    visitedProblems = {}
    wrongSubmissions = {}
    for problem in submissions:
        if(problem['verdict'] != 'OK'):
            if(problem['problem']['name'] in visitedProblems):
                continue
            visitedProblems[problem['problem']['name']] = 1
            for tags in problem['problem']['tags']:
                if(tags not in wrongSubmissions):
                    wrongSubmissions[tags] = 1
                else:
                    wrongSubmissions[tags] += 1
        else:
            completedProblems[problem['problem']['name']] = 1
    
    req_problem_tags = []
    for tags in sorted(wrongSubmissions.items(), key=lambda x: x[1], reverse=True):
        req_problem_tags.append(tags[0])
        if(len(req_problem_tags) == 2):
            break

    weakTags = {}
    min_rating = rank - 100
    max_rating = rank + 300
    if(rank < 1000):
        req_problem_tags.append('brute force')
        req_problem_tags.append('sorting')
        req_problem_tags.append('math')
    if(rank < 1200):
        req_problem_tags.append('sorting')
        req_problem_tags.append('math')
        req_problem_tags.append('greedy')
        req_problem_tags.append('implementation')
        req_problem_tags.append('constructive algorithms')
    elif(rank < 1400):
        req_problem_tags.append('number theory')
        req_problem_tags.append('greedy')
        req_problem_tags.append('constructive algorithms')
        req_problem_tags.append('binary search')
    elif(rank < 1600):
        req_problem_tags.append('strings')
        req_problem_tags.append('binary search')
        req_problem_tags.append('dp')
        req_problem_tags.append('combinatorics')
    elif(rank < 1900):
        req_problem_tags.append('dp')
        req_problem_tags.append('graphs')
        req_problem_tags.append('trees')
        req_problem_tags.append('dfs and similar')
    elif(rank < 2100):
        req_problem_tags.append('dp')
        req_problem_tags.append('graphs')
        req_problem_tags.append('trees')
        req_problem_tags.append('dfs and similar')
    elif(rank < 2400):
        req_problem_tags.append('dp')
        req_problem_tags.append('graphs')
        req_problem_tags.append('fft')
        req_problem_tags.append('geometry')
    elif(rank < 2600):
        req_problem_tags.append('dp')
        req_problem_tags.append('graphs')
        req_problem_tags.append('trees')
        req_problem_tags.append('dfs and similar')
    else:
        req_problem_tags.append('dp')
        req_problem_tags.append('graphs')
        req_problem_tags.append('trees')
        req_problem_tags.append('dfs and similar')
    
    for tag in req_problem_tags:
        weakTags[tag] = getProblems(tag, rank, min_rating, max_rating)
        if(len(weakTags) == 7):
            break
    return weakTags


def getProblems(tag, rank, min_rating, max_rating):
    problems = []
    url = requests.get(
        'https://codeforces.com/api/problemset.problems?tags='+tag)
    jsonData = url.json()
    data = json.dumps(jsonData)
    allData = json.loads(data)
    allProblems = allData['result']['problems']
    allproblemStatistics = allData['result']['problemStatistics']

    count = 0
    lengthOfProblemSet = len(allProblems)
    j = 0
    alreadySuggested = {}
    while(j < lengthOfProblemSet):
        j += 1
        i = random.randint(0, lengthOfProblemSet-1)
        if("points" in allProblems[i] and allProblems[i]['points'] <= 1000):
            continue
        elif (allProblems[i]['index'] == 'A'):
            continue
        if tag in allProblems[i]['tags']:
            if((allProblems[i]['name'] not in alreadySuggested) 
            and (allProblems[i]['name'] not in completedProblems)
            and (allProblems[i].get('rating', 0) >= min_rating)
            and (allProblems[i].get('rating', 0) <= max_rating)
            ):
                alreadySuggested[allProblems[i]['name']] = 1
                tempList = []
                tempList.append(allProblems[i]['name'])
                tempList.append('https://codeforces.com/problemset/problem/' +
                                str(allProblems[i]['contestId'])+'/'+allProblems[i]['index'])
                problems.append(tempList)
                count += 1
        if(count == 6):
            break
    return problems
