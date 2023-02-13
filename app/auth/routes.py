from . import auth


@auth.route("/")
def login():
    return "Login"
