from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from ..models import db, Memo
from ..forms import MemoForm
from flask_login import login_required, current_user

# memoのBlueprint
memo_bp = Blueprint('memo',__name__,url_prefix='/memo')

#======================================================================================
# ルーティング
#======================================================================================
# 一覧
@memo_bp.route("/")
@login_required
def index():
    #メモ全件取得
    memos = Memo.query.filter_by(user_id=current_user.id).all()
    #画面遷移
    return render_template("memo/index.html",memos=memos)

# 登録(Form使用)
@memo_bp.route("/create",methods=["GET","POST"])
@login_required
def create():
    # Formインストール生成
    form = MemoForm()
    if form.validate_on_submit():
        # データ入力取得
        title = form.title.data.strip()
        content = form.content.data

        exists = Memo.query.filter_by(user_id=current_user.id, title=title).first()
        if exists:

            msg = "そのタイトルは既に存在します。別のタイトルにしてください。"
            if msg not in form.title.errors:
                form.title.errors.append(msg)
            return render_template("memo/create_form.html", form=form)


        #登録処理
        memo=Memo(title=title, content=content, user_id=current_user.id)
        db.session.add(memo)
        db.session.commit()
        # フラッシュメッセージ
        flash("登録しました")
        #画面遷移
        return redirect(url_for("memo.index"))
    # GET
    # 画面遷移
    return render_template("memo/create_form.html",form = form)

#更新(Form使用)
@memo_bp.route("/update/<int:memo_id>",methods=["GET","POST"])
@login_required
def update(memo_id):
    # データベースからmemo_idに一致するメモを取得し、
    # 見つからない場合は404エラーを表示
    target_data = Memo.query.get_or_404(memo_id)

    if target_data.user_id != current_user.id:
        abort(403)
    # Formに入れ替え
    form = MemoForm(obj=target_data)

    if form.validate_on_submit():
        new_title = form.title.data.strip()
        new_content = form.content.data

        if new_title != target_data.title:
            dup = Memo.query.filter_by(user_id=current_user.id, title=new_title).filter(
                Memo.id != target_data.id).first()
            if dup:
                msg = "そのタイトルは既に存在します。別のタイトルにしてください。"
                if msg not in form.title.errors:
                    form.title.errors.append(msg)
                return render_template("memo/update_form.html", form=form, edit_id=target_data.id)
        # 更新并提交
        target_data.title = new_title
        target_data.content = new_content
        db.session.commit()
        # フラッシュメッセージ
        flash("変更しました")
        # 画面遷移
        return redirect(url_for("memo.index"))
    # GET時
    # 画面遷移
    return render_template("memo/update_form.html", form=form , edit_id =target_data.id)

#　削除
@memo_bp.route("/delete/<int:memo_id>")
@login_required
def delete(memo_id):
    # データベースからmemo_idに一致するメモを取得し、
    # 見つからない場合は404エラーを表示
    memo = Memo.query.get_or_404(memo_id)
    if memo.user_id != current_user.id:
        abort(403)
    # 削除処理
    db.session.delete(memo)
    db.session.commit()
    # フラッシュメッセージ
    flash("削除しました")
    # 画面遷移
    return redirect(url_for("memo.index"))


