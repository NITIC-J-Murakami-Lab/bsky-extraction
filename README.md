# bsky-extraction

Bluesky.socialからデータをダウンロードするためのプログラムです．後々Mongo DBのようなDBへの保存機能も追加する予定．現状は取得したファイルをそのまま`./data`配下へシリアライズします．


## 準備

まずはプロジェクトのルートディレクトリへ移動．
```sh
$ cd /path/to/bsky_extraction
$ ls 
 config   data   pyproject.toml   README.md   requirements-dev.lock   requirements.lock   script   src
```

### uvで開発環境を同期する
Pythonのパッケージマネージャとして[uv](https://docs.astral.sh/uv/)を利用します．（以前は[rye](https://rye.astral.sh/)を利用していましたが，修正しました．）
```sh
$ uv sync
```
### 任意のアカウントのベアラートークンを作成する
```sh
$ uv run script/get_accessJwt.py メールアドレス パスワード
```
ベアラートークンを組めたコンフィグファイルは`./config`の下に保存される．
`./config/hogehoge.yaml`のようなファイルが作成されているはずです．適宜短いファイル名に修正してください．

## データのダウンロード

### 任意のクエリを検索してダウンロードする

例えばhogeアカウントで作成したベアラートークンを用いて，`柔道 since:2024-07-26T00:00:00 until:2024-08-12T00:00:00`を検索する場合：
```sh
$ uv run script/keyword_extraction.py "柔道 since:2024-07-26T00:00:00 until:2024-08-12T00:00:00" --config hoge.yaml
```

あとは放置するだけ．

#### 注意
[bskyの検索クエリの書き方をまとめてくださっている記事](https://scrapbox.io/Bluesky/%E6%A4%9C%E7%B4%A2%E3%82%AF%E3%82%A8%E3%83%AA)に，`sort`というキーワードが示されていた．これを利用するとポストを収集できないので注意．

### すべてのポストを収集する
w.i.p.
