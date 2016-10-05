from flask import jsonify
from app import admin_login_blueprint

@admin_login_blueprint.route('/login')
def route_login():
    return jsonify({})
