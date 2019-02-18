
from flask import Flask
from flask_script import Manager

from app.models import db
from app.user_views import user_blue

app = Flask(__name__)

app.register_blueprint(blueprint=user_blue, url_prefix='/user')

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/aj8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = '123asfdsgfsdf9ujk'

manage = Manager(app)

if __name__ == '__main__':
    manage.run()
