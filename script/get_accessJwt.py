import requests
import argparse
import yaml

def get_bsky_config(
    identifier:str, 
    password:str, 
    api_login_endpoint:str = "https://bsky.social/xrpc/com.atproto.server.createSession",
    ) -> dict[str, str]:
    
    payload = {
        "identifier": identifier,
        "password": password
    }
    response = requests.post(api_login_endpoint, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("APIトークンを取得しました")
    else:
        print(f"エラーが発生しました")
        print(response.text)
        return {}

    did = data["did"]
    accessJwt = data["accessJwt"]
    return {"did": did, "accessJwt": accessJwt}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process identifier and password.')
    parser.add_argument('identifier', type=str, help='The identifier')
    parser.add_argument('password', type=str, help='The password')
    parser.add_argument('--config_filename', type=str, help='The config file name without extension', default=None)
    args = parser.parse_args()

    identifier = args.identifier
    password = args.password
    config_filename = args.config_filename

    config = get_bsky_config(identifier, password)
    
    if config_filename is None:
        config_filename = f'{identifier}.yaml'
    else:
        config_filename = f'{config_filename}.yaml'
    
    config_filename = f'config/{config_filename}'
    
    with open(config_filename, 'w') as file:
        yaml.dump(config, file)

    print(f"コンフィグファイルを保存しました: {config_filename}")
