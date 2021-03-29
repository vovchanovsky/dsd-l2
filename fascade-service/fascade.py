import uuid
import requests
from flask import Flask, request, redirect
import random

app = Flask(__name__)


@app.route('/')
def not_found():
    return redirect("/fascade_service", code=302)


@app.route('/fascade_service', methods=['GET', 'POST'])
def fascade():
    random.shuffle(log_port_list)
    if request.method == 'POST':
        try:
            if request.json.get('msg'):
                content = {str(uuid.uuid4()): request.json.get('msg')}
                requests.post(f'http://localhost:{log_port_list[0]}/log', json=content)
                return 'OK'
            else:
                return 'Bad Request', 400
        except:
            return 'Internal Server Error', 500

    else:
        result = None
        for port in log_port_list:
            try:
                get_log = requests.get(f'http://localhost:{port}/log')
                get_mes = requests.get('http://localhost:5003/')
                result = get_log.content.decode("utf-8") + '<br/>' + get_mes.content.decode("utf-8")
                return result, 200
                break
            except:
                pass
        if not result:
            return 'Internal Server Error', 500


if __name__ == '__main__':
    log_port_list = [5005, 5006, 5007]
    app.run(port=5001, debug=True)
