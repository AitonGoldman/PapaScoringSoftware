import os
from lib_v2 import roles_constants

def bootstrap_initial_app_tables(table_proxy):
    table_proxy.create_user('test_pss_admin_user',
                            'test_first_name',
                            'test_last_name',
                            'password',
                            event_creator=True,
                            commit=True)
    table_proxy.create_role(roles_constants.TOURNAMENT_DIRECTOR)

