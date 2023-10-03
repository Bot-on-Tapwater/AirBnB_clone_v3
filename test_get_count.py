import json
import requests

if __name__ == "__main__":
    """ get the state without cities
    """
    r = requests.get("http://127.0.0.1:5000/api/v1/states")
    r_j = r.json()
    
    state_id = None
    for state_j in r_j:
        rs = requests.get("http://127.0.0.1:5000/api/v1/states/{}/cities".format(state_j.get('id')))
        rs_j = rs.json()
        if len(rs_j) == 0:
            state_id = state_j.get('id')
            break
    
    if state_id is None:
        print("State without cities not found")
    
    """ Fetch cities
    """
    r = requests.get("http://127.0.0.1:5000/api/v1/states/{}/cities".format(state_id))
    print("state id is ", state_id)
    r_j = r.json()
    print("r_js is ", r_j)
    print(type(r_j))
    print(len(r_j))