#!/bin/bash
# set -eux
set -eu
# usage
cmdname=`basename $0`
function usage()
{
  echo "Usage: ${cmdname} env " 1>&2
  echo 'env: "dev" or "stg" (default: "dev")' 1>&2
  return 0
}

# check options
if [ $# -gt 1 ]; then
  usage
  exit 1
fi

ENV_NAME="dev"
if [ $# -ge 1 ]; then
  case $1 in
    'dev')
      ENV_NAME="dev";;
    'stg')
      ENV_NAME="stg";;
    * )
      usage
      exit 1;;
  esac
fi

# 現在日時でスナップショット出力用のディレクトリ名を生成
OUTPUT_DIR=$(TZ=UTC-9 date '+%y%m%d_%H%M%S')
echo $OUTPUT_DIR

# ログファイルの初期化
LOG_DIR='/docker-pytest/results/'${ENV_NAME}'/'${OUTPUT_DIR}

mkdir -p $LOG_DIR
chmod -R 777 $LOG_DIR

LOG_FILE=$LOG_DIR'/stdout.log'
: > $LOG_FILE
ERR_LOG_FILE=$LOG_DIR'/stderr.log'
: > $ERR_LOG_FILE

# sample
pytest tests/sample/ -v -s --capture=no --env=$ENV_NAME --outdir=$OUTPUT_DIR >>$LOG_FILE 2>>$ERR_LOG_FILE
