from . import db
from flask import jsonify, make_response

class UtilHelper(object):

    @staticmethod
    def check_for_empty_variables(*data):
        ''' Check if any of the variables has a data variable that is empty '''
        empty_status = False
        for variable in data:
            if len(str(variable)) <= 0:
                empty_status = True
                break
        return empty_status

    @staticmethod
    def check_empty_database_table(table_name):
        ''' return the count of the table in the database '''
        table_count = db.session.query(table_name).count()
        if table_count > 0:
            return False
        return True

    @staticmethod
    def check_row_id_exists_in_table(table_name, table_field, field_value):
        db_table_obj = None
        if table_field == 'menu_id':
            db_table_obj = table_name.query.filter_by(menu_id=field_value).first()
        else:
            db_table_obj = table_name.query.filter_by(meal_id=field_value).first()

        if db_table_obj is not None:
            return True
        return False

    @staticmethod
    def check_for_request_params(request_data, *request_keys):
        status = True
        for key in request_keys:
            if key not in request_data:
                status = False
                break
        return status

    @staticmethod
    def validate_exceeds_length(name, required_length):
        if len(name) > required_length:
            return True
        return False
