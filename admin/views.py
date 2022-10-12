from flask_admin.contrib.sqla import ModelView

from sqlalchemy import func

from fastapi_core.users.models import User, Account

from fastapi_core.users.security import hash_password

# async def async_get_users(self):
#         query = select(User).options(selectinload(User.account))
#         result = await self.db.execute(query)
#         return result.scalars().all()

class MyUserAdmin(ModelView):
  column_exclude_list = ('hashed_password',)
  form_columns = ('username', 'firstname', 'lastname', 'email', 'hashed_password',)

  form_args = {
    'hashed_password': {
        'label': 'Password'
    }
}
  
  def create_model(self, form):
    form_fields = form.__dict__['_fields']
    user = User(username=form_fields.username,
                email=form_fields.email,
                hashed_password=hash_password(form_fields.password),
                firstname=form_fields.firstname,
                lastname=form_fields.lastname
    )
            
    # account_type = user_in.__dict__.get('account_type', "standart")
    db_user_account = Account(type="standart", user_id=user.id)
    db_user_account.user = user
    self.db.add_all([user, db_user_account])
    # self.session.add(model)
    self.session.commit()
    # return super().create_model(form)
    return []



  # async def get_query(self):
  #       print(self.session.query(self.model))
  #       return self.session.query(self.model)

  # async def get_count_query(self):
  #       print(self.session.query(func.count('*')).select_from(self.model))
  #       return self.session.query(func.count('*')).select_from(self.model)