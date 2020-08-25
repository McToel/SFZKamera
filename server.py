from flask import Flask, render_template, send_from_directory
from waitress import serve
import os
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def favicon():
    app.send_static_file('latest.jpg')
    return send_from_directory(os.path.join(app.root_path, 'static'), 'latest.jpg')

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    serve(app, host='0.0.0.0', port=5000)