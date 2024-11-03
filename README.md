# Automatic Commit Message Generation Script

This script analyzes staged changes in Git and uses the OpenAI API to automatically generate an appropriate commit message and commit it.

## Prerequisites

- Python 3.7.1 or later
- OpenAI API key
- Git installed

## Setup Instructions

1. **Set up Python environment**: Install Python 3.7.1 or later. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Obtain an OpenAI API key**: Create an account on [OpenAI’s official website](https://openai.com/) and obtain your API key.

3. **Install required libraries**: Run the following command to install the necessary Python library.

   ```bash
   pip install openai
   ```

4. **Set up API key**: Set the obtained API key as the environment variable `OPENAI_API_KEY`. Run the following command in the terminal:

   ```bash
   export OPENAI_API_KEY='your_api_key_here'
   ```

   Replace `your_api_key_here` with your actual API key.

## Usage

1. **Place the script**: Place this script file in the root directory of your Git repository.

2. **Stage changes**: Stage the changes you want to commit.

   ```bash
   git add .
   ```

3. **Run the script**: Execute the script.

   ```bash
   python autoCommitMsg.py
   ```

   The script will analyze the staged changes, use the OpenAI API to generate an appropriate commit message, and automatically commit the changes.

## Notes

- **Managing the API key**: Since the API key is sensitive information, manage it securely using environment variables or configuration files.

- **Diff size**: If there’s a large diff, it may exceed the API’s token limit. Summarizing the diff when necessary can help manage this.

- **Error handling**: Errors may occur during API calls or when running Git commands. Implement proper error handling as needed.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

# 自動コミットメッセージ生成スクリプト

このスクリプトは、Git のステージングされた変更内容を解析し、OpenAI の API を使用して適切なコミットメッセージを自動生成し、コミットを行います。

## 前提条件

- Python 3.7.1 以上
- OpenAI API キー
- Git がインストールされていること

## セットアップ手順

1. **Python 環境の構築**: Python 3.7.1 以上をインストールしてください。[Python 公式サイト](https://www.python.org/downloads/)からダウンロードできます。

2. **OpenAI API キーの取得**: [OpenAI の公式サイト](https://openai.com/)でアカウントを作成し、API キーを取得してください。

3. **必要なライブラリのインストール**: 以下のコマンドを実行して、必要な Python ライブラリをインストールします。

   ```bash
   pip install openai
   ```

4. **API キーの設定**: 環境変数 `OPENAI_API_KEY` に取得した API キーを設定します。 以下のコマンドをターミナルで実行してください。

   ```bash
   export OPENAI_API_KEY='your_api_key_here'
   ```

   `your_api_key_here` を実際の API キーに置き換えてください。

## 使い方

1. **スクリプトの配置**: このスクリプトファイルを、Git リポジトリのルートディレクトリに配置します。

2. **ステージング**: コミットしたい変更をステージングします。

   ```bash
   git add .
   ```

3. **スクリプトの実行**: スクリプトを実行します。

   ```bash
   python autoCommitMsg.py
   ```

    スクリプトはステージングされた変更内容を解析し、OpenAI の API を使用して適切なコミットメッセージを生成し、自動的にコミットを行います。

## 注意事項

- **API キーの管理**: API キーは機密情報です。環境変数や設定ファイルを使用して安全に管理してください。

- **差分のサイズ**: 大きな差分を送信すると、API のトークン制限に達する可能性があります。必要に応じて差分を要約するなどの工夫が必要です。

- **エラーハンドリング**: API の呼び出しや Git コマンドの実行時にエラーが発生する可能性があります。適切なエラーハンドリングを実装してください。

## ライセンス

このプロジェクトは MIT ライセンスの下で提供されています。詳細は LICENSE ファイルをご覧ください。
