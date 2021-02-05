#!/bin/bash
set -eu
# usage
cmdname=`basename $0`
function usage()
{
  echo "Usage: ${cmdname} baseDir compareDir " 1>&2
  echo 'baseDir, compareDir: directory name where results are stored ' 1>&2
  return 0
}

# パラメータチェック
if [ $# -ne 2 ]; then
  usage
  exit 1
fi
BASE_DIR_NAME=$1
COMP_DIR_NAME=$2

# 画像比較対象外テストケース
IGNORE_CASES=("xxxxx" "yyyyy")

BASEDIR="/docker-compare/results"
BASE_DIR="${BASEDIR}/${BASE_DIR_NAME}"
COMP_DIR="${BASEDIR}/${COMP_DIR_NAME}"

function is_ignore_case() {
  file_name=$1
  for prefix in "${IGNORE_CASES[@]}"
  do
    if [ ${file_name:0:3} = $prefix ]; then
      echo 1
      return
    fi
  done

  echo 0
  return
}

# ディレクトリ存在チェック
if [ ! -e $BASE_DIR ]; then
  echo "'${BASE_DIR}' is not exists" 1>&2
  exit 1
fi

if [ ! -e $COMP_DIR ]; then
  echo "'${COMP_DIR}' is not exists" 1>&2
  exit 1
fi

# 結果出力用ディレクトリの作成
OUTPUT_DIR="${BASE_DIR}/compare_${COMP_DIR_NAME/\//\_}"
mkdir -p $OUTPUT_DIR

cd $OUTPUT_DIR

# COMP_DIRのファイルをチェック
for file in `\find $COMP_DIR -maxdepth 1 -name '*.png'`; do
  filename=`basename $file`
  resultname=`basename $file .png`

  # 対象のファイルがチェック対象外の場合、スキップ
  is_ignore_case=`is_ignore_case ${resultname}`
  if [ $is_ignore_case -eq 1 ]; then
    continue
  fi

  FILE_BASE="${BASE_DIR}/${filename}"
  FILE_COMP="${COMP_DIR}/${filename}"

  # FILE_BASEが存在しなければ、FILE_COMPからコピーして削除されたものとして扱う
  if [ ! -e $FILE_BASE ]; then
    echo $re
    cp $FILE_COMP ./
    mv "./${filename}" "./${resultname}_remove.png"
  fi
done

# BASE_DIRのファイルをチェック
for file in `\find $BASE_DIR -maxdepth 1 -name '*.png'`; do
  filename=`basename $file`
  resultname=`basename $file .png`

  # 対象のファイルがチェック対象外の場合、スキップ
  is_ignore_case=`is_ignore_case ${resultname}`
  if [ $is_ignore_case -eq 1 ]; then
    continue
  fi

  FILE_BASE="${BASE_DIR}/${filename}"
  FILE_COMP="${COMP_DIR}/${filename}"
  
  echo $resultname
  if [ ! -e $FILE_COMP ]; then
    # FILE_COMPが存在しなければ、FILE_BASEからコピーして新規作成されたものとして扱う
    cp $FILE_BASE ./
    mv "./${filename}" "./${resultname}_new.png"
  else
    # FILE_COMPが存在すれば、gazosanで比較した結果を出力する
    gazosan "${BASE_DIR}/${filename}" "${COMP_DIR}/${filename}" $resultname --create-change-image
  fi
done

