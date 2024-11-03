import subprocess
import os
from openai import OpenAI

client = OpenAI()

# OpenAI APIキーを環境変数から取得
client.api_key = os.getenv('OPENAI_API_KEY')

if not client.api_key:
    raise ValueError("環境変数 'OPENAI_API_KEY' が設定されていません。")

# ステージングされたファイルの一覧を取得
result = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True)
files = result.stdout.strip().split('\n')

if not files or files == ['']:
    print("ステージングされた変更がありません。")
    exit(1)

# 各ファイルの変更前後の内容を取得
file_diffs = {}

for file in files:
    try:
        # 変更前の内容を取得
        old_version = subprocess.run(['git', 'show', f'HEAD:{file}'], capture_output=True, text=True)
        old_content = old_version.stdout

        # 変更後の内容を取得
        with open(file, 'r') as f:
            new_content = f.read()

        file_diffs[file] = {'old': old_content, 'new': new_content}
    except Exception as e:
        print(f"ファイル '{file}' の処理中にエラーが発生しました: {e}")

# プロンプトの作成
prompt = "以下は、各ファイルの変更前と変更後の内容です。これらの変更に基づいて、適切なコミットメッセージを日本語で生成してください。先頭行は全体像が見えるような簡潔な内容にして、詳細は段落を分けて説明してください。\n"

for file, contents in file_diffs.items():
    prompt += f"\nファイル名: {file}\n変更前:\n{contents['old']}\n変更後:\n{contents['new']}\n"

# OpenAI APIを呼び出し
try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたは優秀なソフトウェアエンジニアです。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.5
    )

    # コミットメッセージとして使用
    commit_message = response.choices[0].message.content.strip()

    # コミットの実行
    subprocess.run(['git', 'commit', '-m', commit_message])
    print("コミットが正常に作成されました。")
except Exception as e:
    print(f"OpenAI APIの呼び出し中にエラーが発生しました: {e}")
