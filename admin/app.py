from flask_admin import Admin
from flask import Flask
from fastapi_core.courses.models import Category, Course, CourseTool
from fastapi_core.users.models import User
from fastapi_core.base import Base
from .admin_db import get_session, sync_engine
from .views import MyCategoryAdmin, MyCourseAdmin, MyToolAdmin, MyUserAdmin
from flask_basicauth import BasicAuth


flask_app = Flask(__name__)
flask_app.config["TEMPLATES_AUTO_RELOAD"] = True
flask_app.config["BASIC_AUTH_FORCE"] = True
flask_app.config["BASIC_AUTH_USERNAME"] = "admin"
flask_app.config["BASIC_AUTH_PASSWORD"] = "adminov"
flask_app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
admin = Admin(flask_app, name="course_hunter", template_mode="bootstrap3")


basic_auth = BasicAuth(flask_app)


admin.add_view(MyUserAdmin(User, next(get_session())))
admin.add_view(MyCategoryAdmin(Category, next(get_session())))
admin.add_view(MyCourseAdmin(Course, next(get_session())))
admin.add_view(MyToolAdmin(CourseTool, next(get_session())))


if __name__ == "__main__":
    Base.metadata.create_all(sync_engine)
    flask_app.run(debug=True, host="0.0.0.0")
