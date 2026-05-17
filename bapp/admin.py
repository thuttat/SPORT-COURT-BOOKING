from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect
from bapp import app, db
from bapp.models import UserRole, Service


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

    def inaccessible_callback(self, name, **kwargs):
        return redirect('http://localhost:5173/login')

class ServiceView(AdminView):
    column_list = ['id', 'name', 'price', 'unit', 'is_active']
    column_searchable_list = ['name']
    column_filters = ['name', 'price', 'unit']
    column_editable_list = ['name', 'price', 'unit', 'is_active']
    form_columns = ['id', 'name', 'price', 'unit', 'is_active']
    can_create = True

admin = Admin(app=app, name='Advanced system', url='/admin')

admin.add_view(ServiceView(Service, db.session, name='Service', endpoint='service'))