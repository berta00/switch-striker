from src.utilities import configuration
from src.core import manager

import os
import flask
import flask_session
import threading


app = flask.Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = 'super_secret'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.logger.disabled = True

flask_session.Session(app)
current_port = configuration.get_web_server_port()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        form_username = flask.request.form['username']
        form_password = flask.request.form['password']

        #TODO: implement db authentication
        if form_username == form_password == 'root':
            flask.session['username'] = form_username
            return flask.redirect('/')

    return flask.render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    flask.session.pop('username')
    return flask.redirect('/login')


@app.route('/', methods=['GET'])
def index():
    if not flask.session.get('username'):
        return flask.redirect('/login')
    
    return flask.render_template('dashboard.html')


def run():
    current_port = configuration.get_web_server_port()

    flask_thread = FlaskThread()
    flask_thread.daemon = True
    flask_thread.start()
    print(flask_thread)
    return flask_thread


def status():
    if(manager.web_server_thread == None):
        return 'off'
    
    return 'running :' + current_port


class FlaskThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            app.run(port=current_port, debug=False, use_reloader=False, threaded=True)
        finally:
            manager.web_server_thread = None
        
    def stop(self):
        if not self.server:
            return False
            
        self.server.shutdown()
        self.thread.join(timeout=5)
        self.server = None
        self.thread = None
        
        manager.web_server_thread = None
        return True

