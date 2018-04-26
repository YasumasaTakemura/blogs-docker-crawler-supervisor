#!/usr/bin/env bash

set -e

flg=$#
SOURCE_IMAGE=$1

usage_exit() {
        if [  $flg -eq  0 ] || [ -z $SOURCE_IMAGE ];then
            echo "Usage: bash $0 -s <SOURCE_IMAGE> [-p <PROJECT_ID> ] ..." 1>&2
            exit 1
        fi
}

set_env(){
    export `cat ./env/.env | grep -v ^# | xargs`
}


# validation
usage_exit

# set env
set_env

# check args
while getopts p:s:h OPT
do
    case $OPT in
        p)  PROJECT_ID=$OPTARG
            ;;
        s)  SOURCE_IMAGE=$OPTARG
            usage_exit
            ;;
        h)  usage_exit
            ;;
        \?) usage_exit
            ;;
    esac
done

docker build -t $SOURCE_IMAGE .
docker tag supervisor gcr.io/$PROJECT_ID/$SOURCE_IMAGE
gcloud docker -- push gcr.io/$PROJECT_ID/$SOURCE_IMAGE