import requests, time, json

URL = "https://0fde11bc.ngrok.io"
UUID = "123e4567-e89b-12d3-a456-426655440000"

def main():
    current_state = {"brew_button": None, "temperate": None}
    while True:
        time.sleep(5)
        actions = get_latest()
        print(actions)
        actions_performed = []
        for item in actions:
            execute_action(item, actions_performed, current_state)
        post_actions(actions_performed, current_state)

def execute_action(item, actions_performed, current_state):
    
    if (True):
        item['status'] = "completed"
    else:
        item['status'] = "failed"
    
    actions_performed.append(item)

def get_latest():
    r = requests.get(URL + "/queued/" + UUID)
    return r.json()["queued_actions"]

def post_actions(actions_performed, current_state):
    ## Jsonify actions_performed, and POST
    data = {}
    data['current_state'] = current_state
    data['actions_performed'] = actions_performed
    r = requests.post(URL + "/perform/" + UUID, json = data, )
    return r.json()

if __name__ == '__main__':
    main()
