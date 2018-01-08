import pymongo
import os
from optparse import OptionParser
import datetime
import configparser
import json 

def listToJson(risk_list):
    file = open('/folk/yli14/nightly.json', 'w') 
    file.write('[\n') 
    for i in risk_list: 
        json_i = json.dumps(i) 
        file.write(json_i) 
        file.write(',\n') 
    file.write('{}\n') 
    file.write(']') 

def data2mongoDB(options):
    path = options.folder
    domain = options.domain
    files = list(os.listdir(path))
    dataList = []
    for f in files:
        dataList = []
        if(f.endswith('.ini')):
            f = os.path.join(path,f)
            dataList = parseIniFile(options, f)
            listToJson(dataList)
            inputMongo(domain, dataList)


def parseIniFile(arg, file):
    recordsList = []
    mergeDict = {}
    confDict = {}
    dataDict = {}
    cf = configparser.ConfigParser()
    cf.read(file)
    sections = cf.sections()
    for s in sections:
        if(s.find("TestCase") == -1):
            options = cf.options(s)
            for opt in options:
                value = cf.get(s, opt)
                confDict[opt] = value
            # add some common keys which are from the arguments
            confDict["project"] = arg.prj
            confDict["release"] = arg.release
            confDict["domain"] =  arg.domain
            confDict["testerName"] = arg.tester
#confDict["spin"] = arg.spin
            confDict["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for s in sections:
        if (s.find("TestCase") >= 0):
            dataDict.clear()
            options = cf.options(s)
            dataDict['testsuite'] = s.split('Case')[1]
            confDict["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            confDict["spin"] = arg.spin 
            for opt in options:
                value = cf.get(s, opt)
                dataDict[opt] = value
            mergeDict = dict(confDict.items() | dataDict.items())
            recordsList.append(mergeDict)
            print(recordsList)
    return recordsList

def inputMongo(domain, dataList):
    connection=pymongo.MongoClient("128.224.154.129", 27017)
    db = connection.sys
    db.authenticate("sys", "sys")
#    db.authenticate("ssp", "ssp")
    if domain.lower() == "usb":
        collection = db.usb
    if domain.lower() == "fs":
        collection = db.fs
    if domain.lower() == "tcpblast":
        collection = db.tcpblast
    if domain.lower() == "sys_level":
        collection = db.sys_level
    if domain.lower() == "test_report":
        collection = db.test_report
    if domain.lower() == "bcopyfill":
        collection = db.bcopyfill
    if domain.lower() == "network":
        collection = db.network_new
    collection.insert(dataList)



if __name__ == '__main__':

    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option('--folder', '-f', dest='folder',
                      help='[REQUIRED] Provide path which store the .ini fiels')
    
    parser.add_option('--project', '-p', dest='prj',
                      help='[REQUIRED] Provide project infomation. example: vx7')
   
    parser.add_option('--domain', '-d', dest='domain',
                      help='[REQUIRED] Provide project infomation. example: fs, usb, network')
    
    parser.add_option('--release', '-r', dest='release',
                      help='[REQUIRED] Provide dvd information, example: SR0490, SR0500')
    
    parser.add_option('--spin', '-s', dest='spin',
                      help='[REQUIRED] Provide spin timestrmp information, example: , ')

    parser.add_option('--tester', '-t', dest='tester',
                      help='[REQUIRED] Provide tester name, example: mliu4')
    (options, args) = parser.parse_args()

    if len(args) != 0:
        parser.error("incorrect number of arguments")

    if not options.folder or not options.prj or not options.domain or not options.release or not options.spin or not options.tester:
        parser.parse_args(['-h'])

    domain = ['usb','fs', 'network', 'tcpblast', 'bcopyfill', 'sys_level','test_report']
    if options.domain.lower() not in domain:
        print("***The domain is not correct***")
        parser.parse_args(['-h'])

    data2mongoDB(options)
