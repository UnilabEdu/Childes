from flask_admin.contrib.sqla import ModelView


class UserView(ModelView):
    can_delete = False
    can_edit = False
    edit_modal = True
    column_display_all_relations = True
