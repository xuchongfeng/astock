from flask import request, make_response

from app import create_app

app = create_app()

@app.before_request
def option_autoreply():
    """Always reply 200 on OPTIONS request"""
    if request.method == 'OPTIONS':
        resp = make_response()
        resp.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有来源
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        resp.headers['Access-Control-Max-Age'] = '1728000'
        resp.headers['Access-Control-Allow-Headers'] = '*'
        return resp

if __name__ == '__main__':
    app.run(debug=True)