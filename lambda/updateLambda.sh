#!/bin/bash

PROFILE="slater_admin"
TS="$(date +'%Y_%m_%d_%H_%M_%S')"
FILENAME="$1_$TS"
REPO_PATH="slater_back"

while getopts ":p" opt; do
    case $opt in
      p)
	echo "-p was triggered!" >&2
	;;
      \?)
	echo "invalid option: -$OPTARG" >&2
	;;
    esac
done

echo "reseting to $REPO_PATH/lambda home"
cd ~/$REPO_PATH/lambda

echo "source virtualenv"
source ~/envs/$1/bin/activate

which python | cat

cd $1
pip install -r requirements.txt

cd ~/envs/$1/lib/python2.7/site-packages
zip -r9 ~/$REPO_PATH/lambda/$1/$FILENAME.zip *

cd ~/envs/$1/lib64/python2.7/site-packages
zip -r9 ~/$REPO_PATH/lambda/$1/$FILENAME.zip *

cd ~/$REPO_PATH/lambda/$1
zip -g $FILENAME.zip handler.py


echo "calling aws update"
aws lambda update-function-code --function-name $1 --zip-file fileb://$FILENAME.zip --publish --region $2 --profile $PROFILE
