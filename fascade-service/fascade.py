import uuid
import requests
from flask import Flask, request, redirect
import random
import pika

app = Flask(__name__)


@app.route('/')
def not_found():
    return redirect("/fascade_service", code=302)


@app.route('/fascade_service', methods=['GET', 'POST'])
def fascade():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    random.shuffle(log_port_list)
    if request.method == 'POST':
        try:
            if request.json.get('msg'):
                content = {str(uuid.uuid4()): request.json.get('msg')}
                for port in log_port_list:
                    try:
                        requests.post(f'http://localhost:{port}/log', json=content)
                        channel.basic_publish(exchange='', routing_key='fascade-msg', body=str(request.json.get('msg')))
                        return 'OK'
                        break
                    except:
                        pass
            else:
                return 'Bad Request', 400
        except:
            return 'Internal Server Error', 500

    else:
        random.shuffle(msg_port_list)
        for msg_port in msg_port_list:
            try:
                get_mes = requests.get(f'http://localhost:{msg_port}/')
                break
            except:
                pass
        for port in log_port_list:
            try:
                get_log = requests.get(f'http://localhost:{port}/log')
                break
            except:
                pass
        try:
            result = 'Reply from  logging-service (port:' + str(port) + '): ' + get_log.content.decode("utf-8") + '<br/>' + \
                     'Reply from messages-service (port:' + str(msg_port) + '): ' + get_mes.content.decode("utf-8")
            return result, 200
        except:
            return 'Internal Server Error', 500


if __name__ == '__main__':
    log_port_list = [5005, 5006, 5007]
    msg_port_list = [5003, 5004]
    app.run(port=5001, debug=True)
