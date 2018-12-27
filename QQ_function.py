import requests
import json

dst_port = 5000;

#return group list like [[name,id],[name,id],...]
def get_group_list():
    group_name_id = []
    response = requests.get('http://127.0.0.1:'+str(dst_port)+'/openqq/get_group_basic_info')
    p = response.text
    text = json.loads(p)
    for each_group in text:
        group_name_id.append([each_group["name"],each_group["id"]])
    return group_name_id


#group_id and message should be string type
def send_group_message(group_id, message):
    dst_url = "http://127.0.0.1:"+str(dst_port)+"/openqq/send_group_message"
    try:
        print("Sending qq group message...")
        response = requests.get(dst_url, params={'id': str(group_id), 'content': message})
        print("Success!")
        #print(response.text)
    except:
        pass
    
    
def send_friend_message(friend_id, message):
    dst_url = "http://127.0.0.1:"+str(dst_port)+"/openqq/send_friend_message"
    try:
        print("Sending friend qq message...")
        response = requests.get(dst_url, params={'id': str(friend_id), 'content': message})
        print("Success!")
        #print(response.text)
    except:
        pass
    

def send_discuss_message(group_id, message):
    dst_url = "http://127.0.0.1:"+str(dst_port)+"/openqq/send_discuss_message"
    try:
        print("Sending qq discuss message...")
        response = requests.get(dst_url, params={'id': str(group_id), 'content': message})
        print("Success!")
        #print(response.text)
    except:
        pass
    
    
def stop_client():
    dst_url = "http://127.0.0.1:"+str(dst_port)+"/openqq/stop_client"
    try:
        print("Stop QQ...")
        response = requests.get(dst_url)
        print("Stop QQ client Success!")
        #print(response.text)
    except:
        pass