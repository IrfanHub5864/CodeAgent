def authenticate_user(username, password):
    """Authenticate a user with username and password."""
    # Bug: missing return statement - always returns None
    if username == "admin" and password == "password":
        print("Login successful")
    else:
        print("Login failed")

def handle_login_request(request):
    """Handle login form submission."""
    username = request.get("username")
    password = request.get("password")

    # Bug: calls authenticate_user but doesn't check return value
    authenticate_user(username, password)

    # Always redirects to dashboard regardless of auth result
    return {"redirect": "/dashboard"}