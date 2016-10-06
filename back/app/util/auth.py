from flask_login import current_user,LoginManager

def generate_user_loader(app):    
    @app.Login_Manager.user_loader    
    def load_user(userid):    
        return app.tables.User.query.get(int(userid))

def init_login_manager(app):
    Login_Manager = LoginManager()
    Login_Manager.init_app(app)
    app.Login_Manager = Login_Manager
    generate_user_loader(app)
