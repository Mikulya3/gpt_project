from fastapi import FastAPI
from sqladmin import Admin, ModelView
from database.models import User
from database.db import engine


app = FastAPI()

admin = Admin(app, engine, name="Admin Panel", url="/admin")


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.email]
    can_create = True   
    can_edit = True
    can_delete = True
    can_view_details = True 
    can_export = True
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_searchable_list = ['name', 'email']
    column_filters = ['name', 'email']


admin.add_view(UserAdmin) 