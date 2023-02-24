from . import auth


@auth.route("/login")
def login():
    return "Login"


@auth.route("/login", methods=["POST"])
def login_post():
    return "Login Post"


@auth.route("/logout")
def logout():
    return "Logout"
