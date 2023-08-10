from flask import Flask, render_template_string, redirect, url_for, request, session
 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

# Flask app setup
app = Flask(__name__)
app.secret_key = 'some_secret_key'  # In production, use a random value.

# Sample hardcoded users
users = {
    "admin": "password"
}

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dash_redirect'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dash_redirect'))
        else:
            return "Invalid credentials, please try again."
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard/')
def dash_redirect():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect('/dash/')

@login_required 
@app.route('/dash/')
def dash_redirect():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect('/dash/')

# Dash app setup
dash_app = Dash(__name__, server=app, url_base_pathname='/dash/')
dash_app.layout = html.Div([
    html.H1("Welcome to the Dash app!"),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'NYC'},
            ],
            'layout': {
                'title': 'Sample Dash Data Visualization'
            }
        }
    ),
    html.A("Logout", href='/logout')
])

if __name__ == '__main__':
    app.run(debug=True, port=8060)