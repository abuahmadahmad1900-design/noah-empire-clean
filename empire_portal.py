from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'empire_magic_entrance.html')

@app.route('/splash')
def splash():
    return send_from_directory('.', 'final_splash.html')

@app.route('/<path:filename>')
def files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
