from __future__ import division
import re
import sys 
import urllib 
import json 
import datetime
import os,os.path,datetime 
from pymongo import MongoClient

def get15before():
    now = datetime.datetime.now()
    beforeDay = now + datetime.timedelta(days=-10)
    return beforeDay.strftime("%Y-%m-%d")

def getCovNew(covBaseDir):
    base_dir = covBaseDir
    l=os.listdir(base_dir) 
    l.sort(key=lambda fn: os.path.getmtime(base_dir+fn) if not os.path.isdir(base_dir+fn) else 0) 
    d=datetime.datetime.fromtimestamp(os.path.getmtime(base_dir+l[-1])) 
    newCovFile = l[-1]
    newCovFile2 = newCovFile.split('.')[0]
    return newCovFile2
'''
def dicToJsonFile(load_dict):
    json_str = json.dumps(load_dict)
    dictC = json.loads(json_str)
    json.dump(dictC, open('/folk/yli14/userinfoJson.txt', 'w'))
    str = '[' + json_str + ']'
    dictC = json.loads(str)
    json.dump(dictC, open('/folk/yli14/userinfo.txt', 'w'))
'''
def getPieValue():
    file = open('/folk/yli14/nightly.ini')
    lines = file.readlines()
    for line in lines:
        if line.split(' = ')[0]== 'Not Started':
           dict['notstart'] = line.split(' = ')[1].split('    #')[0]
        if line.split(' = ')[0]== 'Pass':
            dict['pass'] = line.split(' = ')[1].split('    #')[0]
        if line.split(' = ')[0]== 'Fail':
            dict['fail'] =  line.split(' = ')[1].split('    #')[0]
        if line.split(' = ')[0]== 'Blocked':
            dict['blocked'] =  line.split(' = ')[1].split('    #')[0]
        if line.split(' = ')[0]== 'Will Not Run':
            dict['willnotrun'] =  line.split(' = ')[1].split('    #')[0]
        if line.split(' = ')[0]== 'Total':
            dict['total'] =  line.split(' = ')[1].split('    #')[0]
            break 
    pa = int(dict['pass'])
    fail = int(dict['fail'])
    notstart = int(dict['notstart'])
    total = int(dict['total'])
    dict['pass'] = int(dict['pass']) 
    dict['fail'] = fail 
    dict['notstart'] = notstart
    dict['blocked'] = int(dict['blocked'])

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getLogUrl(url):
    text = getHtml(url)
    url2 = re.findall('http\w*://.+?/*>', text)
    url = url2[2]
    logUrl = url.split('>')[0]
    return logUrl
    
def parseWarnHtml(url):
    txt = getHtml(url)
    APIGEN = re.findall(r"APIGEN:  (.+?)<",txt)
    Diab = re.findall(r"Diab:  (.+?) GNU",txt)
    GNU = re.findall(r"GNU:  (.+?)<",txt)
    RPMs = re.findall(r"RPMs:  (.+?)<",txt)
    listWarn = APIGEN + Diab + GNU + RPMs
    listWarn = map(eval, listWarn)
    print listWarn 
    sum1 = sum(listWarn)
    return sum1
    
def parseTreeHtml(TreeUrl):
    html = getHtml(TreeUrl)
    warnHtmlName = re.findall(r"this, '(.+?)>Warnings",html)
    print warnHtmlName[0].split('\'')[0]
    return warnHtmlName[0].split('\'')[0]

def getWarnNum(baseUrl):
    tree01HtmlUrl = baseUrl + 'TREE_0001.html'   
    warnHtmlUrl = baseUrl + parseTreeHtml(tree01HtmlUrl)
    print warnHtmlUrl
    return parseWarnHtml(warnHtmlUrl)

def warnInsert():
    dict['warnnum'] = getWarnNum(dict['logBaseUrl']) 
    dict['testsuite'] = "Spininfo" 
    dict['spin'] = dict['nightlyspin'] 
    conn = MongoClient('mongodb://sys:sys@128.224.154.129:27017/sys')    #connect to mongodb
    db = conn.sys
    db.test_report.insert(dict)
        
def dicToJsonFile(load_dict):
    json_str = json.dumps(load_dict)
    dictC = json.loads(json_str)
    json.dump(dictC, open('/folk/yli14/test/runOrNot.json', 'w'))
    str = '[' + json_str + ']'
    dictC = json.loads(str)
    json.dump(dictC, open('/folk/yli14/test/runOrNot2.json', 'w'))

def getTodayInfo():
    configUrl = 'http://pek-vx-nightly1/buildarea1/pzhang1/jenkinsEnvInjection/vx7_nightly_spin.config'
    configUrlCi = 'http://pek-vx-nightly1/buildarea1/pzhang1/jenkinsEnvInjection/vx7_ci_nightly_spin.config'
    dict = {}

    page = urllib.urlopen(configUrl)
    str = page.read()
    NIGHTLYSPIN = re.findall(r"NIGHTLYSPIN=(.+?)\n",str)
    lastS = re.findall(r"lastS=(.+?)\n",str)
    LTAFRELEASE = re.findall(r"LTAFRELEASE=(.+?)\n",str)
    timestamp = re.findall(r"timestamp=(.+?)\n",str)
    if NIGHTLYSPIN:
        dict['nightlyspin'] = NIGHTLYSPIN[0] 
    else:
        dict['nightlyspin'] = 'null:(no spin builded)' 
    dict['lastspin'] = lastS[0] 
    dict['lastspinFake'] = lastS[0] 
    dict['ltafrelease'] = LTAFRELEASE[0] 
    dict['nightlytime'] = timestamp[0] 
    
    page = urllib.urlopen(configUrlCi)
    str = page.read()
    ciSpin = re.findall(r"NIGHTLYSPIN=(.+?)\n",str)
    if (len(ciSpin) != 0) and (len(NIGHTLYSPIN) != 0) and (ciSpin[0] != dict['nightlyspin']):
        dict['getcidata'] = "yes"
    else:
        dict['getcidata'] = "no"
        
    if len(NIGHTLYSPIN) == 0:
        dict['getcfg1data'] = "no"
        dict['cfg1col'] = "red.png"
        print "red code ! config file nightlySpin is empty"
    else:
        dict['getcfg1data'] = "yes"
        dict['cfg1col'] = "blue.png"
        print "config file nightlySpin is not empty"

    print sys.argv[1]
    if (sys.argv[1] == '14'):
        dict['lastspinFake'] = NIGHTLYSPIN[0] 
    else:
        pass
    dicToJsonFile(dict)
    os.system("expect /folk/yli14/test/cp55.exp")
    os.system("cat /folk/yli14/test/runOrNot2.json")

def getDataToDb():
    page = urllib.urlopen(configUrl)
    str = page.read()
    NIGHTLYSPIN = re.findall(r"NIGHTLYSPIN=(.+?)\n",str)
    lastS = re.findall(r"lastS=(.+?)\n",str)
    LTAFRELEASE = re.findall(r"LTAFRELEASE=(.+?)\n",str)
    timestamp = re.findall(r"timestamp=(.+?)\n",str)
    print NIGHTLYSPIN, lastS, LTAFRELEASE, timestamp 
    timestamp1 = timestamp[0]
    timestamp = timestamp1[0:8]
    dict['nightlytime'] = timestamp
    if NIGHTLYSPIN:
        dict['nightlyspin'] = NIGHTLYSPIN[0] 
        dict['commiturl'] = 'http://pek-vx-nightly1/buildarea1/pzhang1/jenkinsEnvInjection/' + dict['nightlyspin'] + '_churn_email.html'
        dict['logUrl'] = getLogUrl(dict['commiturl'])
        dict['logBaseUrl'] = dict['logUrl'].split('index')[0]
    else:
        print "config file 's nightspin is null"

    if LTAFRELEASE[0] == "vx7-integration":
        print "vx7-integration"
        baseUrl = "http://ctu-hig4.wrs.com/folk/hzeng/CoverityRuns/871/VxWorks" + " 7/"
        covBaseDir = "/net/ctu-rhfs1/ctu-rhfs03/home03/hzeng/CoverityRuns/871/VxWorks 7/"
    elif LTAFRELEASE[0] == "vx7-SR0520-features":
        print "vx7-SR0520-features"
        baseUrl = "http://ctu-hig4.wrs.com/folk/hzeng/CoverityRuns/662/Vx7-SR0520/"
        covBaseDir = "/net/ctu-rhfs1/ctu-rhfs03/home03/hzeng/CoverityRuns/662/Vx7-SR0520/"
    else:
        print "error ! "
        baseUrl = "code need be updated "
        
    dict['covnew'] = getCovNew(covBaseDir) 
    dict['covpdfurl'] = baseUrl + dict['covnew'] + '.pdf';
    dict['covpngurl'] = baseUrl + dict['covnew'] + '.png';
    dict['ltafrelease'] = LTAFRELEASE[0] 
    dict["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    endTime = timestamp[0:4] + '-' + timestamp[4:6] + '-' + timestamp[6:8] 
    before15 = get15before()
    dict['trendurl'] = 'http://pek-lpgtest3.wrs.com/ltaf/nightly_interface.php?release_name=' + dict['ltafrelease'] + '&f_type=chart&start_date=' + before15 + '&end_date=' + endTime 
    cmdGetIni = 'curl -o /folk/yli14/nightly.ini "http://pek-lpgtest3.wrs.com/ltaf/nightly_interface.php?release_name=' + dict['ltafrelease'] + '&f_type=info&date=' + endTime + '"'
    dateFormat = '/folk/yli14/test/dataFormat.sh'
    nightlyInputDb = "%s %s" % ('python3 /folk/yli14/test/genericScript.py -f /folk/yli14/test/ -p vx7 -d test_report -r xxx -t yli14 -s ', NIGHTLYSPIN[0])
    cmdGetTrendPic= 'wget -O /folk/yli14/nightlyTrend.png "http://pek-lpgtest3.wrs.com/ltaf/nightly_interface.php?release_name=' + dict['ltafrelease'] + '&f_type=chart&start_date=' + before15  + '&end_date=' + endTime + '"'

    if NIGHTLYSPIN: 
        os.system(cmdGetIni)
        os.system(dateFormat)
        os.system(nightlyInputDb)
#os.system(cmdGetTrendPic)
        getPieValue()
        warnInsert()
        print dict

# Entry point
#os.system("python /folk/yli14/test/dawnJudge.py 14")
print " ############# Entry Point ############"
if (sys.argv[1] == '30'):
    getTodayInfo()
    sys.exit(0)

dict = {}
with open("/folk/yli14/test/runOrNot.json",'r+') as load_f:
    load_dict = json.load(load_f)
    print load_dict
if (load_dict['getcfg1data'] == "yes"):
    configUrl = 'http://pek-vx-nightly1/buildarea1/pzhang1/jenkinsEnvInjection/vx7_nightly_spin.config'
    getDataToDb()
    getTodayInfo()
elif(load_dict['getcidata'] == "yes"):
    configUrl = 'http://pek-vx-nightly1/buildarea1/pzhang1/jenkinsEnvInjection/vx7_ci_nightly_spin.config'
    getDataToDb()
else:
    print "both cfg1 and cfgci file's spin name is null, so nothing to do"

print " ############# The End ############ "
sys.exit(0)
