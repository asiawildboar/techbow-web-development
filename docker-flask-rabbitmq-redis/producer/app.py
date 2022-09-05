from flask import Flask, Response
from flask import jsonify
import pika


app = Flask(__name__)

@app.route("/")
def hello():
    return Response("Hi I am producer service!")

@app.route("/temperature/<int:temperature>", methods=['GET'])
def send_temperature(temperature):
    # validation logic
    if temperature > 100 or temperature < 0:
        # raise alert here
        return jsonify({'action': False, 'reason': 'temperature out of range'}) 
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-host'))
    channel = connection.channel()
    channel.queue_declare(queue='demo-temperature')
    channel.basic_publish(exchange='',
                          routing_key='demo-temperature',
                          body=str(temperature))

    return jsonify({'action': True, 'temperature': temperature})

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
