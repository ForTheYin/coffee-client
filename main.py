import requests, time, json, giphy_client, webbrowser
from giphy_client.rest import ApiException
from pprint import pprint
from GPIOLibrary import GPIOProcessor

URL = "https://292c54ac.ngrok.io/"
UUID = "123e4567-e89b-12d3-a456-426655440000"

GP = GPIOProcessor()

def main():
    # get_gif()
    current_state = {"brew_button": None, "temperature": None, "strength_button": None}
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
        current_state['brew_button'] = "brewing"
    elif (item['action'] == "switch_brew"):
        item['status'] = "completed" if setStrongMode() else "failed"
        current_state['strength_button'] = "strong" if current_state['strength_button'] == "regular" else "regular"
    
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
    return r #.json()

def get_gif():
    api_instance = giphy_client.DefaultApi()
    api_key = 'dc6zaTOxFJmzC' # str | Giphy API Key.
    tag = 'coffee' # str | Filters results by specified tag. (optional)
    rating = 'g' # str | Filters results by specified rating. (optional)
    fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    try: 
        # Random Endpoint
        api_response = api_instance.gifs_random_get(api_key, tag=tag, rating=rating, fmt=fmt)
        webbrowser.open_new_tab(api_response.data.image_url)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_random_get: %s\n" % e)

def brewCoffee():
    print("Brewing Coffee!")
    Pin25 = GP.getPin25()
    Pin25.out()
    
    try:
        Pin25.high()
        time.sleep(0.3)
        Pin25.low()
        return True
    except:
        return False
    finally:
        GP.cleanup()


def setStrongMode():
    print("Strong mode chosen!")
    Pin24 = GP.getPin24()
    Pin24.out()

    try:
        Pin24.high()
        time.sleep(0.3)
        Pin24.low()
        return True
    except:
        return False
    finally:
        GP.cleanup()



if __name__ == '__main__':
    main()
