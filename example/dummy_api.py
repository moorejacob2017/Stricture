from flask import Flask, request, jsonify
import multiprocessing
import time
import uuid

# DummyAPI

app = Flask(__name__)

processes = {}

#======================================================
# UTIL AND COUNTER FUNCTION
def get_process_by_id(process_id):
    global processes
    if process_id in processes:
        return processes[process_id]
    else:
        return None
#---------------------------------------------------
def count_seconds(counter, pause_event):
    start_time = time.time()
    while True:
        if not pause_event.is_set():
            current_time = time.time()
            elapsed_time = current_time - start_time
            counter.value = int(elapsed_time)
            if elapsed_time >= 1000000: 
                break
        time.sleep(1)
#======================================================
# API FUNCTIONS
# curl -X GET http://localhost:5000/api/launch
@app.route('/api/launch', methods=['GET'])
def launch():
    global processes
    process_id = str(uuid.uuid4())
    counter = multiprocessing.Value('i', 0)
    pause_event = multiprocessing.Event()
    process = multiprocessing.Process(target=count_seconds, args=(counter, pause_event))
    process.start()
    processes[process_id] = {'process': process, 'counter': counter, 'pause_event': pause_event}
    return jsonify({'message': 'Counting process launched.', 'process_id': process_id}), 200
#---------------------------------------------------
# curl -X POST -H "Content-Type: application/json" -d '{"process_id": "<process_id_here>"}' http://localhost:5000/api/pause
@app.route('/api/pause', methods=['POST'])
def pause():
    process_id = request.json.get('process_id', None)
    if process_id:
        proc = get_process_by_id(process_id)
        if proc and proc['process'].is_alive():
            proc['pause_event'].set()
            return jsonify({'message': 'Counting process paused.'}), 200
    return jsonify({'message': 'Invalid process ID or process not found.'}), 400
#---------------------------------------------------
# curl -X POST -H "Content-Type: application/json" -d '{"process_id": "<process_id_here>"}' http://localhost:5000/api/resume
@app.route('/api/resume', methods=['POST'])
def resume():
    process_id = request.json.get('process_id', None)
    if process_id:
        proc = get_process_by_id(process_id)
        if proc and proc['process'].is_alive():
            proc['pause_event'].clear()
            return jsonify({'message': 'Counting process resumed.'}), 200
    return jsonify({'message': 'Invalid process ID or process not found.'}), 400
#---------------------------------------------------
# curl -X GET http://localhost:5000/api/status?process_id=<process_id_here>
@app.route('/api/status', methods=['GET'])
def status():
    process_id = request.args.get('process_id', None)
    if process_id:
        proc = get_process_by_id(process_id)
        if proc and proc['process'].is_alive():
            return jsonify({'elapsed_time_seconds': proc['counter'].value}), 200
        else:
            return jsonify({'message': 'Counting process not active or completed.'}), 400
    return jsonify({'message': 'Invalid process ID.'}), 400
#======================================================
if __name__ == '__main__':
    app.run(debug=False)