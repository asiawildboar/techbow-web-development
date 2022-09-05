from flask import Flask, Response, request
import redis

app = Flask(__name__)

redis_client = redis.Redis(host='redis-host', port=6379, db=0)

@app.route('/set')
def set():
    key = request.args.get("key")
    value = request.args.get("value")
    if key is None or value is None:
        return 'OOps, the key or value is NULL'
    redis_client.set(key, value)
    return 'OK. We have set ' + key + ' to be ' + value

@app.route('/get')
def get():
    key = request.args.get('key')
    if key is None:
        return 'OOps, the key is null'
    value = redis_client.get(key)
    return value

@app.route("/")
def hello():
    return Response("Hi from your Flask app running in your Docker container!")

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    print("...talk to mysql to authenticate user")
    session_id = hash(username)
    redis_client.set(session_id, username)
    redis_client.expire(session_id, 20)
    return "login success" + str(session_id)

@app.route("/loginBySession")
def loginBySession():
    session_id = request.args.get("session_id")
    username = request.args.get("username")
    username_retrieved = redis_client.get(session_id)
    if username_retrieved is None:
        return "session expired"
    if username == username_retrieved:
        return "session not matched"
    return "login success"

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
