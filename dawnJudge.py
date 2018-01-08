import sys 
import os 
import re
import urllib 
import json 

def dicToJsonFile(load_dict):
    json_str = json.dumps(load_dict)
    dictC = json.loads(json_str)
    json.dump(dictC, open('/folk/yli14/test/runOrNot.json', 'w'))
    str = '[' + json_str + ']'
    dictC = json.loads(str)
    json.dump(dictC, open('/folk/yli14/test/runOrNot2.json', 'w'))

def runOrNot():
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
    print dict
    
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
#dict['getcfg1data'] = "no"
#dict['getcidata'] = "no"
    else:
        pass
    dicToJsonFile(dict)
#os.system("expect /folk/yli14/test/cp55.exp")
    os.system("cat /folk/yli14/test/runOrNot2.json")
    print "\n end"
    sys.exit(0)

runOrNot()
