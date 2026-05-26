# Google翻訳ツール (CLI & Web GUI)

Google翻訳API（`deep-translator`ライブラリ経由）を利用した、シンプルで使いやすいPython向け翻訳ツールです。コマンドラインインターフェース (CLI) とWebベースのグラフィカルユーザーインターフェース (GUI) の両方を提供します。
Google Cloudの公式APIキーは不要で、無料で制限なく利用できます。

## 必要な環境

- Python 3.7以上
- `deep-translator` ライブラリ
- `streamlit` ライブラリ (Web GUI版のみ)

## インストール方法

以下のコマンドを実行して、必要なライブラリをインストールしてください。

```bash
pip install deep-translator streamlit
```

## CLI版の使い方

スクリプト `translator_cli.py` を実行して翻訳を行います。

### 1. テキストの翻訳

```bash
python translator_cli.py "Hello, World!" -t ja
```
**出力:**
```
こんにちは世界！
```

### 2. 元言語と翻訳先言語の指定

`-s` (source) と `-t` (target) オプションで言語を指定できます。デフォルトの元言語は `auto` (自動検出)、翻訳先は `ja` (日本語) です。

```bash
# 日本語から英語への翻訳
python translator_cli.py "こんにちは、世界！" -s ja -t en
```
**出力:**
```
Hello World!
```

### 3. テキストファイルの翻訳

`-f` オプションを使用して、ファイル内のテキストを翻訳できます。

```bash
python translator_cli.py -f input.txt -t en
```

### 4. サポートされている言語の確認

`-l` オプションで、使用可能な言語のリストを表示できます。

```bash
python translator_cli.py -l
```

### CLI版オプション一覧

| 短縮 | フルオプション | 説明 | デフォルト値 |
|:---|:---|:---|:---|
| `-h` | `--help` | ヘルプメッセージを表示 | - |
| `-s` | `--source` | 元の言語 | `auto` |
| `-t` | `--target` | 翻訳先の言語 | `ja` |
| `-f` | `--file` | 翻訳するテキストファイルのパス | - |
| `-l` | `--list-languages`| サポートされている言語のリストを表示 | - |

## Web GUI版の使い方

`translator_web.py` スクリプトを実行し、Webブラウザでアクセスします。

### 1. アプリケーションの起動

以下のコマンドを実行してStreamlitアプリケーションを起動します。

```bash
streamlit run translator_web.py
```

アプリケーションが起動すると、ターミナルに表示されるURL（通常 `http://localhost:8501`）をWebブラウザで開いてください。

### 2. 翻訳の実行

1.  左側のテキストエリアに翻訳したいテキストを入力します。
2.  「元言語」と「翻訳先言語」のドロップダウンから言語を選択します。
3.  「🚀 翻訳実行」ボタンをクリックします。
4.  右側のテキストエリアに翻訳結果が表示されます。

## 注意事項

このツールは `deep-translator` ライブラリを利用しており、非公式な方法でGoogle翻訳にアクセスするため、短時間に大量のリクエストを送信するとIP制限を受ける可能性があります。大量の翻訳を行う場合は、Google Cloud Translation APIなどの公式サービスの利用を検討してください。
