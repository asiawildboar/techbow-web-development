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

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
