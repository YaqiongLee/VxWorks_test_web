#!/bin/bash -x
#
# d.sh - defect report script.
#
# Copyright (c) 2017 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#
# modification history
# --------------------
# 10feb17  h_l  created

# Description:
# ============
# This script generate defect html report.

scriptDir=$(dirname $0)
ISSUE_HTML=$scriptDir/defect.html
if [  $1 == "vx7-i1032-dev" ]
then
    curl -u "svc-ssp:jiradefect" http://jira.wrs.com/issues/?filter=30060 > $ISSUE_HTML
elif [  $1 == "BSP" ]
then
    curl -u "svc-ssp:jiradefect" http://jira.wrs.com/issues/?filter=23486 > $ISSUE_HTML
else
    curl -u "svc-ssp:jiradefect" http://jira.wrs.com/issues/?filter=28000 > $ISSUE_HTML
fi


END_LINE=`awk '/\/table/{print NR - 1}' $ISSUE_HTML`
let END_LINE+=2

sed -i "${END_LINE},\$d" $ISSUE_HTML
#sed -i "1,${START_LINE}d" $ISSUE_HTML
sed -i "1,412d" $ISSUE_HTML

sed -i "s/\/images/http\:\/\/jira.wrs.com\/images/g" $ISSUE_HTML

sed -i "s/\/browse/http\:\/\/jira.wrs.com\/browse/g" $ISSUE_HTML

sed -i "s/\/secure/http\:\/\/jira.wrs.com\/secure/g" $ISSUE_HTML


sed -i "s/td class=\"nav issuekey\"/td class=\"nav issuekey\" width=\"100\"/g" $ISSUE_HTML

sed -i 's/issuetable\"/issuetable\" style=font-family\:Arial/g' $ISSUE_HTML

sed -i -e '/class="priority"/s@<img.*alt="@<a>@g' -e '/class="priority"/s@" title.*@</a>@g' $ISSUE_HTML

