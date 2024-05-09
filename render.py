from flask import *
from hashlib import md5
from sqlitedict import SqliteDict
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

USER_DATABASE = 'user.db'
PRODUCT_DATABASE = 'product.sqlite'

def get_user_db():
    db = getattr(g, '_user_database', None)
    if db is None:
        db = g._user_database = sqlite3.connect(USER_DATABASE)
        db.row_factory = sqlite3.Row
    return db

def get_product_db():
    return SqliteDict(PRODUCT_DATABASE, autocommit=True)


@app.teardown_appcontext
def close_user_connection(exception):
    db = getattr(g, '_user_database', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def close_product_connection(exception):
    db = getattr(g, '_product_database', None)
    if db is not None:
        db.close()


def init_user_db():
    with app.app_context():
        db = get_user_db()
        with app.open_resource('user_schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        print(username, password)
        if "'" in username:
            flash('Invalid Character', 'error')
            return render_template('login.html')

        db = get_user_db()
        cur = db.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{md5(password.encode()).hexdigest()}'")
        user = cur.fetchone()
        if user:
            session['logged_in'] = True
            session['username'] = username
            flash('Login success', 'success')
            return redirect(url_for('index'))
        else:
            flash('username or password incorrect', 'error')
            return render_template('login.html')

    else:
        if 'logged_in' not in session:
            return render_template('login.html')
        else:
            return redirect('/')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('您已登出', 'success')
    return redirect(url_for('index'))

@app.route('/')
def index():
    db = get_product_db()
    products = list(db.items())
    return render_template('index.html', products=products)

@app.route('/download_database')
def download_database():
    if 'logged_in' not in session:
        flash('Login First', 'error')
        return render_template('login.html')
    else:
        return send_file(PRODUCT_DATABASE, as_attachment=True)

@app.route('/upload_database', methods=['POST'])
def upload_database():
    if 'logged_in' not in session:
        flash('Login First', 'error')
        return render_template('login.html')
    else:
        file = request.files['database']
        if file.filename == '':
            flash('未選擇文件', 'error')
            return redirect('/')
        if file:
            file.save(os.path.join(app.root_path, PRODUCT_DATABASE))
            flash('資料庫上傳成功', 'success')
        else:
            flash('上傳失敗', 'error')
        return redirect('/')

if __name__ == '__main__':
    init_user_db()
    app.run(host='0.0.0.0', port=8888)
