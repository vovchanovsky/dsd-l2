from flask import Flask, request
import pika
import docker
from threading import Thread
import time
import sys

app = Flask(__name__)

memory = []


def consumer():
    for i in range(5):  # try 3 times
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='fascade-msg')

            def callback(ch, method, properties, body):
                print(" [x] Received %r" % body.decode())
                memory.append(body.decode())

            channel.basic_consume(queue='fascade-msg', on_message_callback=callback, auto_ack=True)
            print(' [*] All done. Waiting for your messages. To exit press CTRL+C')
            channel.start_consuming()
        except:
            if i % 2 == 0:
                print('Connecting to RabbitMQ... Wait a while.')
            time.sleep(7)
            pass
    print("Cannot connect to RabbitMQ:( Try again later!")
    sys.exit(0)


@app.route('/')
def msg():
    if request.method == 'GET':
        return ', '.join(memory)


if __name__ == '__main__':
    doc_client = docker.from_env()
    try:
        doc_client.containers.get('rabbitmq')
        print("RabbitMQ is already running")
    except:
        container = doc_client.containers.run('rabbitmq:3-management', name='rabbitmq', detach=True,
                                              auto_remove=True, ports={5672: 5672, 15672: 15672})
    try:
        Thread(target=consumer, daemon=True).start()
        app.run(port=sys.argv[1], debug=True, use_reloader=False)
    except:
        print("App run error. Do you include port number in args?")
    finally:
        print("Good luck!")
