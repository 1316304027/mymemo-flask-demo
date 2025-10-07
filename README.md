MyMemo — Flask デモ（ポートフォリオ用）

概要

* シンプルなメモアプリ（Python / Flask）。
* 機能：ユーザー登録・ログイン、メモの作成・編集・削除（ユーザー毎のプライベートメモ）。
* 技術スタック：Python, Flask, Flask-Login, Flask-WTF, SQLAlchemy。

動作確認（ローカル・Windows PowerShell）

1. python -m venv .venv
2. .venv\Scripts\Activate.ps1
3. pip install -r requirements.txt
4. $env:FLASK_APP="my_memo_app.app"
5. $env:FLASK_ENV="development"
6. flask run
   ブラウザで [http://127.0.0.1:5000](http://127.0.0.1:5000) にアクセス。

プロダクション（Render）での起動例

* Start command: `gunicorn my_memo_app.app:app`
* 環境変数に `SECRET_KEY` を設定してください。

注意点

* 本リポジトリにはローカルの SQLite ファイルは含めていません（instance/memodb.sqlite は個人環境で生成されます）。
* データ永続化が必要な場合は、PostgreSQL 等の外部 DB に切り替えてください。

使い方（短いデモ手順）

1. サインアップしてアカウントを作成。
2. ログインして「新しいメモを作成」。
3. メモの一覧で編集・削除を確認。

作者：魏 玉臻
