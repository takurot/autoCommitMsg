import subprocess
import os
import logging
from openai import OpenAI

# ログの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# OpenAI API クライアントの設定
client = OpenAI()

# ステージングされたファイルの一覧を取得
try:
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only'],
        capture_output=True,
        text=True,
        check=True
    )
    files = result.stdout.strip().split('\n')
    if not files or files == ['']:
        logging.info("ステージングされた変更がありません。")
        exit(1)
except subprocess.CalledProcessError as e:
    logging.error(f"git diff の実行中にエラーが発生しました: {e}")
    exit(1)

# 各ファイルの変更前後の内容を取得
file_diffs = {}

for file in files:
    if not os.path.exists(file):
        logging.warning(f"ファイル '{file}' が存在しません。スキップします。")
        continue
    try:
        # 変更前の内容を取得
        old_version = subprocess.run(
            ['git', 'show', f'HEAD:{file}'],
            capture_output=True,
            text=True,
            check=True
        )
        old_content = old_version.stdout

        # 変更後の内容を取得
        with open(file, 'r') as f:
            new_content = f.read()

        file_diffs[file] = {'old': old_content, 'new': new_content}
    except subprocess.CalledProcessError as e:
        logging.error(f"git show の実行中にエラーが発生しました: {e}")
    except Exception as e:
        logging.error(f"ファイル '{file}' の処理中にエラーが発生しました: {e}")

# プロンプトの作成
file_diff_prompts = [
    f"ファイル名: {file}\n変更前:\n{contents['old']}\n変更後:\n{contents['new']}\n"
    for file, contents in file_diffs.items()
]
prompt = "以下は、各ファイルの変更前と変更後の内容です。これらの変更に基づいて、適切なコミットメッセージを英語で生成してください。" \
         "先頭行は全体像が見えるような簡潔な内容にして、詳細は段落を分けて説明してください。\n" + "\n".join(file_diff_prompts)

# OpenAI APIを呼び出し
try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたは優秀なソフトウェアエンジニアです。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.5
    )

    # コミットメッセージの取得
    commit_message = response.choices[0].message.content.strip()

    # コミットメッセージの長さを確認
    if len(commit_message) > 72:
        logging.warning("生成されたコミットメッセージが長すぎます。手動で修正してください。")
        exit(1)

    # コミットの実行
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)
    logging.info("コミットが正常に作成されました。")

except subprocess.CalledProcessError as e:
    logging.error(f"git commit の実行中にエラーが発生しました: {e}")
    exit(1)
except Exception as e:
    logging.error(f"予期しないエラーが発生しました: {e}")
    exit(1)
