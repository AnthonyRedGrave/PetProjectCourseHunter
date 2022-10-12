from flask_admin import Admin
from flask import Flask
from fastapi_core.users.models import User
# from fastapi_core.db import async_get_db, get_session
from .admin_db import get_session
from .views import MyUserAdmin


flask_app = Flask(__name__)
flask_app.config['TEMPLATES_AUTO_RELOAD'] = True
admin = Admin(flask_app, name='course_hunter', template_mode='bootstrap3')


admin.add_view(MyUserAdmin(User, next(get_session())))


if __name__ == "__main__":
    flask_app.run(debug=True, host='0.0.0.0')