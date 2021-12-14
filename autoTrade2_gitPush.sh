#!/bin/bash
source /home/ubuntu/.bashrc

date=$(date)
github_id=$env_github_id
github_Token=$env_github_Token
github_Address=$env_autoTrade_git
Project_name="autoTrade2"
logFile="/home/ubuntu/"$Project_name"_push.log"
export SourceDir=$env_autoTrade_Dir

cd $SourceDir
sleep 0.1

echo "========= push Start (Date : $date) =========" && echo "========= push Start (Date : $date) =========" >$logFile 2>&1
echo "git add . ..." && echo "git add . ..." >>$logFile 2>&1
echo "$(git add .)" >>$logFile 2>&1
echo "" && echo "" >>$logFile 2>&1 && echo "==" >>$logFile 2>&1

echo "git status" && echo "git status" >>$logFile 2>&1
echo "$(git status)" >>$logFile 2>&1
echo "" && echo "" >>$logFile 2>&1 && echo "==" >>$logFile 2>&1

# Choose Commit Type [#
source $SourceDir./Choose_Commit_Type.sh
sleep 0.1
# Choose Commit Type ]#
echo ""
# Enter Commit Title [#
printf "Enter Commit Title : "
read Commit_Title
Commit_Msg="$env_CType $Commit_Title"
# Enter Commit Title ]#

echo "git commit -m $Commit_Msg" && echo "git commit -m $Commit_Msg" >>$logFile 2>&1
echo "$(git commit -m "$Commit_Msg")" >>$logFile 2>&1
echo "" && echo "" >>$logFile 2>&1 && echo "==" >>$logFile 2>&1

echo "git push!" && echo "git push!" >>$logFile 2>&1
git push https://$github_id:$github_Token@$github_Address >>$logFile 2>&1

sleep 2

result="$(awk '/Everything up-to-date/' $logFile 2>&1)"
echo "$result"

if [ -z "$result" ]; then
  echo "git push Success~!" && echo "git push Success~!" >>$logFile 2>&1
  echo "========= push OK (Date : $date) =========" && echo "========= push OK (Date : $date) =========" >>$logFile 2>&1
else
  echo "!! git push ERROR! please check $logFile !!" && echo "!! git push ERROR! please check $logFile !!" >>$logFile 2>&1
fi

exit 0
