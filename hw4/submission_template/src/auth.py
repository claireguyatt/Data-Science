def get_user(request_handler):
    username = request_handler.get_argument("username")
    password = request_handler.get_argument("password")
    if username != "nyc" or password != "iheartnyc":
        return None
    print(username)
    return username

def get_login_url(request_handler):
    pass