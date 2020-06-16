import hashlib
from functools import wraps

from flask import Flask, request, render_template, abort

app = Flask(__name__)


def get_token_auth_header():
    # @TODO unpack the request header
    if 'Authorization' not in request.headers:
        abort(401)

    auth_headers = request.headers['Authorization']
    header_parts = auth_headers.split(' ')

    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        abort(401)

    return header_parts[1]


def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt = get_token_auth_header()
        return f(jwt, *args, **kwargs)

    return wrapper


@app.route('/')
def index():
    name = 'Mclord'
    return render_template('index.html', name=name)


@app.route('/headers')
@requires_auth
def headers(jwt):
    print(jwt)
    return 'not implemented'


word = 'blueberry'
md5 = '8bea7325cb48514196063a1f74cf18a4'
hashed_word = hashlib.md5(word.encode()).hexdigest()
print(hashed_word)

if md5 == hashed_word:
    print('Password Accepted')
else:
    print('Incorrect Password')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
