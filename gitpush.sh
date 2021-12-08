#!/bin/bash
date=`date`
github_id="hunmin815"
github_Token="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"
dir="/home/ubuntu/autoTrade2/"
echo "git add . ..." > push.log 2>&1
git add . >> push.log 2>&1
echo "" >> push.log 2>&1

echo "git status" >> push.log 2>&1
echo `git status` >> push.log 2>&1
echo "" >> push.log 2>&1

echo "git commit -m $date commit" >> push.log 2>&1
echo `git commit -m "$date commit"` >> push.log 2>&1
echo "" >> push.log 2>&1

echo "git push!" >> push.log 2>&1
echo `git clone https://$github_id:$github_Token@github.com/hunmin815/autoTrade.git` >> push.log 2>&1

result=`awk '/Unpacking objects: 100%/ && /done./' $dir"push.log"`


if [ -z "$result"];then
	echo "!! git push ERROR! please check push.log !!" >> push.log 2>&1
else
	echo "git push Success~!" >> push.log 2>&1
fi

exit 0
