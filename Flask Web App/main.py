from website import create_app
from flask import session, redirect, url_for

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode