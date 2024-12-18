# bsky-extraction

まずはプロジェクトのルートディレクトリへ移動．
```sh
$ cd /path/to/bsky_extraction
$ ls 
 config   data   pyproject.toml   README.md   requirements-dev.lock   requirements.lock   script   src
```

## 準備
### ryeで開発環境を同期する
```sh
$ rye sync
```
### 任意のアカウントのベアラートークンを作成する
```sh
$ rye run python script/get_accessJwt.py メールアドレス パスワード
```
ベアラートークンを組めたコンフィグファイルは`./config`の下に保存される．

## データのダウンロード

### 任意のクエリを検索してダウンロードする

例えばrsimdアカウントで作成したベアラートークンを用いて，`柔道 since:2024-07-26T00:00:00 until:2024-08-12T00:00:00`を検索する場合：
```sh
$ rye run python script/keyword_extraction.py "柔道 since:2024-07-26T00:00:00 until:2024-08-12T00:00:00" --config rsimd.yaml
```

あとは放置するだけ．

#### 注意
[bskyの検索クエリの書き方をまとめてくださっている記事]https://statics.teams.cdn.office.net/evergreen-assets/safelinks/1/atp-safelinks.html)に，`sort`というキーワードが示されていた．これを利用するとポストを収集できないので注意．

### すべてのポストを収集する
w.i.p.