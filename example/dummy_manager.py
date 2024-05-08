import requests
import time

class DummyAPIManager:
    def __init__(self, api_url):
        self.api_url = api_url
        self.process_id = None
    #---------------------------------------------------
    # curl -X GET http://localhost:5000/api/launch
    def api_launch(self):
        while True:
            try:
                response = requests.get(self.api_url + '/api/launch')
                if response.status_code == 200:
                    data = response.json()
                    self.process_id = data.get('process_id')
                else:
                    raise Exception("API failed to launch process")
                break
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}. Retrying...")
            time.sleep(1)
    #---------------------------------------------------
    # curl -X POST -H "Content-Type: application/json" -d '{"process_id": "<process_id_here>"}' http://localhost:5000/api/pause
    def api_resume(self):
        headers = {'Content-Type': 'application/json'}
        data = {'process_id': self.process_id}
        while True:
            try:
                response = requests.post(self.api_url + '/api/resume', json=data, headers=headers)
                if response.status_code:
                    break  # Break the loop if request reaches api
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}. Retrying...")
            time.sleep(1)
    #---------------------------------------------------
    # curl -X POST -H "Content-Type: application/json" -d '{"process_id": "<process_id_here>"}' http://localhost:5000/api/resume
    def api_pause(self):
        headers = {'Content-Type': 'application/json'}
        data = {'process_id': self.process_id}
        while True:
            try:
                response = requests.post(self.api_url + '/api/pause', json=data, headers=headers)
                if response.status_code:
                    break  # Break the loop if request reaches api
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}. Retrying...")
            time.sleep(1)
    #---------------------------------------------------
    # curl -X GET http://localhost:5000/api/status?process_id=<process_id_here>
    def api_is_alive(self):
        try:
            response = requests.get(self.api_url + '/api/status?process_id=' + self.process_id)
            print(response.text.strip())
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        return True