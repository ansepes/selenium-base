# GUIテスト自動化のベース環境

## 前提

- 開発環境は以下を想定
  - Windows 10
  - VSCode
  - VSCode Remote Development
  - Docker for Windows
- 実行環境は Docker , docker-compose があればOK

## コンテナ構成

- chrome
  - Seleniumの公式イメージ
- pytest
  - ランナー環境
  - テストコードの開発環境
- gazosan
  - 画像比較ツール: gazosanを含む環境
  - スクリーンショットの比較に使用

## 環境ごとの設定ファイル

- 以下ファイルに環境ごとの設定を記述
  - pytest/env/variable.[env].json
- pytest 実行時の引数で環境を指定する想定
  - デフォルトはdev

## 開発環境

- pytest コンテナで VSCode Remote Development 拡張機能を使ってコーディングする想定
  - 開発環境、editer, linterの設定共通化
- Remote Development 環境の設定は以下のファイル。
  - .devcontainer/devcontainer.json
  - .devcontainer/.vscode/settings.json

## PageObjectModel

- オレオレPageObjectModelでサンプル実装
  - pytest/tests/sample/test_sample.py
    - GMailへログインするサンプル
    - 現状はvariable.[env].json に適当なログインID/PASSを追記して使う想定
      - ここはもっと安全な形で環境ごとの情報を持たせるようにしたい
  - 経験上、css selector で指定した element が見つからないエラーが多発するので、なるべくエラー発生箇所が分かりやすくなるよう例外に色々情報を乗せた

## 実行環境の構築
- 適当なOS環境を用意する
  - 今回はCentOS7環境を用意した
- Docker , docker-compose をインストールする
  - 以下サイトを参考にした
    - https://zenn.dev/ymasaoka/articles/install-docker-centos-7
    - https://zenn.dev/ymasaoka/articles/install-docker-compose-centos-7
- ソースを適当な場所に配置する

## テストの実行
- ソースを配置したディレクトリへ移動して以下を実行する
- テスト環境の起動
```
docker-compose up -d --build
```
- 各テストの実行順をコントロールしたい場合
  - 以下スクリプトにて細かく指定する想定
    - pytest/scripts/exec-test.sh
  - 実行するには以下コマンド
    - パラメータ
      - 1: 実行環境( dev / stg  || default: dev)
```
docker-compose exec pytest bash scripts/exec-test.sh dev
```
- pytestを実行する場合
  - 以下コマンドを実行する
      - パラメータ
        - 1: 実行環境( dev / stg  || default: dev)
```
docker-compose exec pytest pytest tests dev
```
- テスト環境の停止
```
docker-compose down
```

## テストの結果確認

- 実行結果の出力先
  - ソース配置ディレクトリ/results/<実行環境>/<現在日時(YYMMDD_hhmmss)> へ実行結果の画面スナップショットやPDF等が格納される
  - stdout.logに出力された結果が全てPASSEDであれば、コードレベルのエラーは無し

## テスト結果スナップショットの比較

- 以下コマンドを実行する
```
docker-compose exec compare bash compare.sh <最新のテスト結果格納ディレクトリ名> <前回のテスト結果格納ディレクトリ名>
```
- <最新のテスト結果格納ディレクトリ> 直下へ以下のディレクトリが作成され、差分があるファイルのみ差分情報のファイルが出力される
  - compare_<前回のテスト結果格納ディレクトリ名>
- 出力されるファイルの種類
  - xxx_delete.png: 前回のテストから消えた部分の表示
  - xxx_add.png: 前回のテストから増えた部分の表示
  - xxx_diff.png: 前回のテストとの差分の表示
  - xxx_remove.png: 前回のテストから消えたテストケースの結果
  - xxx_new.png: 前回のテストから増えたテストケースの結果

- 実行例
```
docker-compose exec compare bash compare.sh dev/210202_174039 dev/210115_121212
```