import requests, time, json
from GPIOLibrary import GPIOProcessor

URL = "https://292c54ac.ngrok.io/"
UUID = "123e4567-e89b-12d3-a456-426655440000"

GP = GPIOProcessor()

def main():
    current_state = {"brew_button": None, "temperature": None}
    while True:
        time.sleep(5)
        actions = get_latest()
        print(actions)
        actions_performed = []
        for item in actions:
            execute_action(item, actions_performed, current_state)
        post_actions(actions_performed, current_state)

def execute_action(item, actions_performed, current_state):
    
    if (item['action'] == "brew"):
        item['status'] = "completed" if brewCoffee() else "failed"
    
    actions_performed.append(item)

def get_latest():
    r = requests.get(URL + "/queued/" + UUID)
    return r.json()["queued_actions"]

def post_actions(actions_performed, current_state):
    ## Jsonify actions_performed, and POST
    data = {}
    data['current_state'] = current_state
    data['actions_performed'] = actions_performed
    r = requests.post(URL + "/perform/" + UUID, json = data)
    return r.json()

def brewCoffee():
    Pin27 = GP.getPin27()
    Pin27.out()

    Pin25 = GP.getPin25()
    Pin25.out()

    try:
        Pin27.high()
        time.sleep(0.3)
        Pin27.low()
        return True
    except:
        return False
    finally:
        GP.cleanup()


if __name__ == '__main__':
    main()
