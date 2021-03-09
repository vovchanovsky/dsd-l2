import uuid
import requests
from flask import Flask, request, redirect

app = Flask(__name__)


@app.route('/')
def not_found():
    return redirect("/fascade_service", code=302)


@app.route('/fascade_service', methods=['GET', 'POST'])
def fascade():
    if request.method == 'POST':
        try:
            if request.json.get('msg'):
                content = {str(uuid.uuid4()): request.json.get('msg')}
                requests.post('http://localhost:5002/log', json=content)
                return 'OK'
            else:
                return 'Bad Request', 400
        except:
            return 'Internal Server Error', 500

    else:
        try:
            getlog = requests.get('http://localhost:5002/log')
            getmes = requests.get('http://localhost:5003/')
            result = getlog.content.decode("utf-8")+'<br/>'+getmes.content.decode("utf-8")
            return result, 200
        except:
            return 'Internal Server Error', 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)
