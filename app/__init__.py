from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    from .views.news import news_bp
    from .views.maps import maps_bp
    from .views.real_estate import real_estate_bp
    from .views.sports import sports_bp

    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(maps_bp, url_prefix='/maps')
    app.register_blueprint(real_estate_bp, url_prefix='/real_estate')
    app.register_blueprint(sports_bp, url_prefix='/sports')

    # 루트 경로에 대한 라우트 추가
    @app.route('/')
    def home():
        return render_template('index.html')

    with app.app_context():
        db.create_all()

    return app
