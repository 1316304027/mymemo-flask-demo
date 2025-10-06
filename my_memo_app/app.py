from flask import Flask,render_template,redirect,url_for
from flask_login import LoginManager,current_user
from flask_migrate import Migrate
from .models import db, User
from .auth.views import auth_bp
from .memo.views import memo_bp


#======================================================================================
# Flask
#======================================================================================
app=Flask(__name__)
# 設定ファイル読み込む
app.config.from_object("my_memo_app.config.Config")
# dbとFlaskとの紐付け
db.init_app(app)

# (SQLAlchemy)データベースの初期化
with app.app_context():
    db.create_all()

# マイグレーションとの紐付け(Flaskとｄｂ)
migrate = Migrate(app, db)

# LoginManagerインスタンス
login_manager = LoginManager()
# LoginManagerとFlaskとの紐付け
login_manager.init_app(app)

#　ログイン必要なページにアクセスしようとしたときに表示されるメッセージを変更
login_manager.login_message="認証していません：ログインしてください"

# 未認証のユーザーがアクセスしようとした際に
# リダイレクトされる関数名を設定する　(ブループリント対応)
login_manager.login_view = "auth.login"

# blueprintをアプリケーションに登録
app.register_blueprint(auth_bp)
app.register_blueprint(memo_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    #if current_user.is_authenticated:
        #return redirect(url_for("memo.index"))
    return render_template("index.html")


# viewsのインポートcd WORK_FLASK/my_memo_app

@app.errorhandler(404)
def show_404_page(error):
    msg=error.description
    print('エラー内容：',msg)
    return render_template('errors/404.html',msg=msg), 404

#======================================================================================
# 実行
#======================================================================================
if __name__=="__main__":
    app.run()
