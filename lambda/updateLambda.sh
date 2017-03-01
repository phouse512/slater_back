#!/bin/bash

PROFILE="slater_admin"
TS="$(date +'%Y_%m_%d_%H_%M_%S')"
REPO_PATH="slater_back"
ADD_PSQL=false
ADD_BCRYPT=false
TO_SHIFT=0

while getopts "p:b" opt; do
    case $opt in
      p)
	echo "-p was triggered!" >&2
	ADD_PSQL=true
	TO_SHIFT=$((TO_SHIFT +1))
	;;
      b)
	echo "-b was triggered!" >&2
	ADD_BCRYPT=true
	TO_SHIFT=$((TO_SHIFT + 1))
	;;
      \?)
	echo "invalid option: -$OPTARG" >&2
	;;
    esac
done

shift $TO_SHIFT
ARG1=$1
ARG2=$2

echo $ARG1
echo $ARG2

FILENAME="${ARG1}_${TS}"

echo "reseting to $REPO_PATH/lambda home"
cd ~/$REPO_PATH/lambda

echo "source virtualenv"
source ~/envs/$ARG1/bin/activate

which python | cat

cd $ARG1
pip install -r requirements.txt

cd ~/envs/$ARG1/lib/python2.7/site-packages
zip -r9 ~/$REPO_PATH/lambda/$ARG1/$FILENAME.zip *

cd ~/envs/$ARG1/lib64/python2.7/site-packages
zip -r9 ~/$REPO_PATH/lambda/$ARG1/$FILENAME.zip *

if [ "$ADD_PSQL" = true ] ; then
    echo "psycopg2 flag set.. zipping up psycopg2"
    cd ~/awslambda-psycopg2
    zip -r9 ~/$REPO_PATH/lambda/$ARG1/$FILENAME.zip psycopg2/
fi

if [ "$ADD_BCRYPT" = true ] ; then
    echo "bcrypt flag set.. zipping up bcrypt"
    cd ~/
    zip -r9 ~/$REPO_PATH/lambda/$ARG1/$FILENAME.zip bcrypt/
    zip -r9 ~/$REPO_PATH/lambda/$ARG1/$FILENAME.zip bcrypt-3.1.1-py2.7.egg-info/
fi

cd ~/$REPO_PATH/lambda/$ARG1
zip -g $FILENAME.zip handler.py

echo "calling aws update"
aws lambda update-function-code --function-name $ARG1 --zip-file fileb://$FILENAME.zip --publish --region $ARG2 --profile $PROFILE
