import subprocess
from openai import OpenAI
client = OpenAI()

# ステージングされた差分を取得
diff = subprocess.check_output(["git", "diff", "--cached"]).decode("utf-8")

# 差分が存在しない場合の処理
if not diff.strip():
    print("ステージングされた変更がありません。")
    exit(1)

# プロンプトの作成
prompt = f"以下のGit差分を基に、適切なコミットメッセージを英語で生成してください:\n{diff}"

# OpenAI APIを呼び出し
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

# コミット実行
subprocess.run(["git", "commit", "-m", commit_message])
