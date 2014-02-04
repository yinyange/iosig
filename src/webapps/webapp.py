import os
import datetime
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello_world(name=None):
    return render_template('hello.html', name=name)
#    return 'Hello World!'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

@app.route('/iosig')
def list_trace_dirs():
    # list the $IOSIG_DATA
    iosig_data_path = os.getenv('IOSIG_DATA')
    if (iosig_data_path == None):
        return render_template('trace_dirs.html', list=None)
    dirs = [ trace_dir for trace_dir in os.listdir(iosig_data_path) if os.path.isdir(os.path.join(iosig_data_path, trace_dir)) ]
    dirs.sort()
    dirs_list = []
    for directory in dirs:
        user, separator, the_rest = directory.partition('_')
        ts_epoch, separator, exe_name = the_rest.partition('_')
        date_string = datetime.datetime.fromtimestamp(float(ts_epoch)).strftime('%Y-%m-%d %H:%M:%S')
        dirs_list.append([user, date_string, exe_name])

    return render_template('trace_dirs.html', list=dirs_list)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')