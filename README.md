# SCRAPY_MEMO
Scrapyのクローリングメモ


## Dockerでの手順
### 今いるディレクトリをマウントして接続
~~~
docker run -t -i -v `pwd`:/usr/src/python python:latest /bin/bash
~~~

### 初期インストール
~~~
apt-get update
pip install --upgrade pip
pip install scrapy
~~~

### プロジェクト作成(プロジェクト名のフォルダが作成される）
~~~
scrapy startproject PROJECT_NAME
~~~

[python超初心者がスクレイピングしてみる](https://qiita.com/ritukiii/items/272d485e8a249d0d1bd7)

### クローリングしたいサイトに合わせてspiderファイルを作成し、実行(プロジェクトフォルダ直下に移動する)
spiderで使用したいライブラリはpipインストールしておく
~~~
scrapy crawl SPIDER_NAME
~~~
CSVに出力
~~~
scrapy crawl SPIDER_NAME -o FILENAME.csv
~~~
