"""
This script performs keyword extraction from posts on the bsky.social platform using the provided query and configuration.
Modules:
    - atproto: Provides client and session management for the API.
    - requests: Used for making HTTP requests to the API.
    - time: Used for handling time-related operations.
    - json: Used for handling JSON data.
    - yaml: Used for handling YAML configuration files.
    - typing: Provides type hints for better code readability.
    - pickle: Used for serializing and deserializing Python objects.
    - argparse: Used for parsing command-line arguments.
Global Variables:
    - searchPosts_endpoint (str): The endpoint URL for searching posts.
CLI Arguments:
    - query (str): The search query string.
    - --prefix (str, optional): The prefix for the output files. Defaults to None.
    - --config (str, optional): The configuration file name. Defaults to "rsimd.yaml".
    - --limit (int, optional): The maximum number of posts to retrieve per request. Defaults to 100.
    - --cursor (str, optional): The cursor for pagination. Defaults to None.
    - --data_root (str, optional): The root directory for saving data. Defaults to "data/".
Script Execution:
    - Parses the CLI arguments.
    - Loads the configuration from the specified YAML file.
    - Sets up the request headers using the access token from the configuration.
    - Constructs the search parameters.
    - Iteratively fetches posts from the API until no more posts are available or an error occurs.
    - Saves the retrieved posts to JSON files in batches of 1000.
    - Saves the final batch of posts and the payload with the last cursor to files.
"""

from atproto import Client, IdResolver, models, SessionEvent, AsyncClient
import requests
import time
import json
import yaml
from typing import Any, Optional
import pickle
from argparse import ArgumentParser

# Global variables
searchPosts_endpoint = "https://bsky.social/xrpc/app.bsky.feed.searchPosts"

# CLI arguments
parser = ArgumentParser()
parser.add_argument("query", type=str)
parser.add_argument("--prefix", type=str, default=None)
parser.add_argument("--config", type=str, default="rsimd.yaml")
parser.add_argument("--limit", type=int, default=100)
parser.add_argument("--cursor", type=str, default=None)
parser.add_argument("--data_root", type=str, default="data/")

# query "柔道 since:2024-07-26T00:00:00 until:2024-08-12T00:00:00 sort"

# script
if __name__ == "__main__":
    # CLI arguments parsing
    args = parser.parse_args()
    with open("config/" + args.config, "r") as f:
        payload = yaml.safe_load(f)
    headers = {"Authorization": f"Bearer {payload["accessJwt"]}"}
    print(headers)
    print("クエリー：", args.query)
    if args.prefix:
        prefix = args.prefix
    else:
        prefix = args.query.split()[0]

    # 設定
    params = {
        "q": args.query,
        "limit": args.limit,
        "cursor": None,
    }
    data_root = "data/"

    # 初期化
    all_posts: list[dict[str, Any]] = []
    cursor = None
    start_index = 0

    # データ取得
    while True:
        if cursor:
            payload["cursor"] = cursor
        response = requests.get(searchPosts_endpoint, headers=headers, params=params)

        if response.status_code != 200:
            data = response.json()
            print(f"エラーが発生しました: {data.get('error', '不明なエラー')}")
            print(f"ステータスコード: {response.status_code}")
            break

        data = response.json()
        posts = data.get("posts", [])
        all_posts.extend(posts)
        print(f"{len(posts)}件の投稿を取得しました。")

        if len(all_posts) >= 1000:
            n_items = len(all_posts)
            path = f"{data_root}/{prefix}_{start_index}({n_items}).json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(all_posts, f, indent=4, ensure_ascii=False)

            start_index += n_items
            all_posts: list[dict[str, Any]] = []
            print(f"データを保存しました: {path}")

    # 最後のデータを保存
    path = f"{data_root}/{prefix}_{start_index}({len(all_posts)}).json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=4, ensure_ascii=False)
    print(f"データを保存しました: {path}")
    print("すべてのデータを取得しました。")
    path = f"{data_root}/{prefix}_payload.pickle"

    with open(path, "wb") as f:
        pickle.dump(payload, f)
    print("最後のカーソルを含めたペイロードを保存しました：", path)

    if cursor is not None:
        path = f"{data_root}/{prefix}_cursor.txt"
        with open(path, "w") as f:
            f.write(cursor)
        print("最後のカーソルを保存しました：", path)
