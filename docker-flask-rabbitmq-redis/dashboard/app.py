from flask import Flask, Response, request
from flask import jsonify
import redis

app = Flask(__name__)

redis_client = redis.Redis(host='redis-host', port=6379, db=0)

@app.route('/getavg')
def get():
    total = int(redis_client.get('total'))
    num = int(redis_client.get('num'))
    avg = total * 1.0 / num
    return jsonify({'avg': avg, 'total': total, 'num': num})

@app.route("/")
def hello():
    return Response("Hi I am dashboard service!")

if __name__ == "__main__":
    app.run("0.0.0.0", port=5002, debug=True)
