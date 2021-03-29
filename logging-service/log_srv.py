from flask import Flask, request
import docker
import hazelcast
import sys

app = Flask(__name__)


@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        req_data = request.json
        print(req_data)
        key = next(iter(req_data.keys()))
        distributed_map.set(key, req_data[key])
        return ''
    else:
        return ','.join(distributed_map.get_all(distributed_map.key_set().result()).result().values())


if __name__ == '__main__':
    container = None
    doc_client = docker.from_env()
    try:
        container = doc_client.containers.get(f"{sys.argv[1]}-hazelcast")
        container.start()
        client = hazelcast.HazelcastClient()
        distributed_map = client.get_map("logs-map")
        app.run(port=sys.argv[1], debug=True)
    except:
        print("Incorrect port number in args. Please restart the program.")
    finally:
        if container:
            container.stop()
        print("Good luck!")
