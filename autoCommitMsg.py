import subprocess
import logging
import sys
from openai import OpenAI
from openai import OpenAIError
import os

# ログの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# OpenAI API クライアントの設定
client = OpenAI()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("環境変数 'OPENAI_API_KEY' が設定されていません。")

# 実行時引数からフォルダーパスを取得
if len(sys.argv) != 2:
    logging.error("使用方法: python script_name.py <フォルダーパス>")
    exit(1)

target_folder = sys.argv[1]

# フォルダがGit管理下にあるか確認
try:
    subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], cwd=target_folder, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    logging.error(f"指定されたフォルダ '{target_folder}' はGitリポジトリではありません。")
    exit(1)

# git diff の出力を取得
try:
    diff_result = subprocess.run(
        ['git', 'diff', '--cached', target_folder],
        capture_output=True,
        text=True,
        check=True
    )
    diff_output = diff_result.stdout.strip()
    print(diff_output)
    if not diff_output:
        logging.info(f"指定されたフォルダ '{target_folder}' にステージングされた変更はありません。")
        exit(1)
except subprocess.CalledProcessError as e:
    logging.error(f"git diff --cached 実行中にエラーが発生しました: {e}")
    exit(1)

# プロンプトの作成
prompt = (
    "以下は、ステージングされた変更の詳細です。これらに基づいて、適切なコミットメッセージを英語で生成してください。\n"
    "先頭行は全体像がわかる簡潔な内容にし、詳細は段落を分けて説明してください。\n\n"
    f"{diff_output}"
)

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

    # コミットメッセージの取得
    commit_message = response.choices[0].message.content.strip()

    print(commit_message)

    # コミットメッセージの長さを確認
    # if len(commit_message) > 200:
    #     logging.warning("生成されたコミットメッセージが長すぎます。手動で修正してください。")
    #     exit(1)

    # コミットの実行
    subprocess.run(['git', 'commit', '-m', commit_message], cwd=target_folder, check=True)
    logging.info("コミットが正常に作成されました。")
except OpenAIError as e:
    logging.error(f"OpenAI API 呼び出し中にエラーが発生しました: {e}")
    exit(1)
except subprocess.CalledProcessError as e:
    logging.error(f"git commit の実行中にエラーが発生しました: {e}")
    exit(1)
except Exception as e:
    logging.error(f"予期しないエラーが発生しました: {e}")
    exit(1)
