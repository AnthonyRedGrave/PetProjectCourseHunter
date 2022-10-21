from flask_admin.contrib.sqla import ModelView

from sqlalchemy import func

# from wtforms import StringField
from wtforms.widgets import TextArea
from wtforms.fields import StringField

from fastapi_core.users.models import User, Account
from fastapi_core.courses.models import Category, Course

from fastapi_core.users.security import hash_password


class MyCourseAdmin(ModelView):
  pass


class MyToolAdmin(ModelView):
  form_columns = ('title',)
  column_exclude_list = ('course')


class MyCategoryAdmin(ModelView):
  form_columns = ('title', 'description')


class MyUserAdmin(ModelView):
  column_exclude_list = ('hashed_password',)
  form_columns = ('username', 'firstname', 'lastname', 'email', 'hashed_password')

  form_args = {
    'hashed_password': {
        'label': 'Password'
    }
  } 

  # form_overrides = {
  #   'account': StringField
  # }

  def scaffold_form(self):
        form_class = super(MyUserAdmin, self).scaffold_form()
        form_class.account_type = StringField('Account type')
        return form_class
  
  def create_model(self, form):
    user = User(username=form.username.data,
                email=form.email.data,
                hashed_password=hash_password(form.hashed_password.data),
                firstname=form.firstname.data,
                lastname=form.lastname.data
    )
            
    db_user_account = Account(type=form.account_type.data, user_id=user.id)
    db_user_account.user = user
    self.session.add_all([user, db_user_account])
    self.session.commit()
    return user
