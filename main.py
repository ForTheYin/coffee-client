import requests, time, json, giphy_client, webbrowser
from giphy_client.rest import ApiException
from pprint import pprint


URL = "https://0fde11bc.ngrok.io"
UUID = "123e4567-e89b-12d3-a456-426655440000"

def main():
    get_gif()
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


if __name__ == '__main__':
    main()
