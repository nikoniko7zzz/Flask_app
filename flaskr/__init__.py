import os

from flask import Flask


def create_app(test_config=None):
    # アプリの作成と設定
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # テストしていないときに、インスタンス設定があればそれをロードする。
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 渡された場合、テストコンフィグをロードします。
        app.config.from_mapping(test_config)

    # インスタンスフォルダが存在することを確認する
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 'Hello, World!'を出すシンプルなページ
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app