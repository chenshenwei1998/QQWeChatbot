import json
import QQ_function
import weixin_function
from wsgiref.simple_server import make_server
import time


server_port = 6088
forward_group_list = []
qqgroup_list = []
weixingroup_list = []
all_group_list = []
state = 1
group_info=""
mass_group=[]
current_notification="Nothing"
admin = "陈沈威"
admin_id=0
concerned_people = []


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))
    request_body = json.loads(request_body.decode('utf-8'))
    
    print(request_body)
    
    post_type = request_body["post_type"]
    
    try:
        if(post_type=="receive_message"):
            message_type = request_body["type"]
            
            if(message_type=="group_message"):
                
                group_id = request_body["group_id"]
                group = request_body["group"]
                content = request_body["content"]
                sender = request_body["sender"]
                print(group +" receive "+content+" from "+sender)
                
                if("通知" in content):
                    send_notification(group_id)
					
                if(sender in concerned_people):
                    QQ_function.send_friend_message(admin_id, sender+"在群”"+group+"“中发送了消息“"+content+"”，快去看看吧！")
                
                saveRecord(group, sender, content)
                
                if(isForwardGroup(group_id)):
                    forwardGroup(group_id, sender, content)
                else:
                    pass
                
            elif(message_type=="friend_message"):
                
                sender_id = request_body["sender_id"]
                sender = request_body["sender"]
                content = request_body["content"]
                print("You receive "+content+" from "+sender)
                
                handle_friend_message(sender, sender_id, content)
                
        else:
            pass
    except:
        print("Some mistake happened!")
 
    dic = {'status': 'OK'}
 
    return [json.dumps(dic)]



def create_qqgroup_list():
    result = []
    print("Getting QQ group list...")
    try:
        result = QQ_function.get_group_list().copy()
        print("Successfully get the QQ group list!")
        print("QQ group list:")
        print(result)
    except:
        print("Fail to get the QQ group list! Make sure you have opened MojoQQ!")
        #sys.exit(-1)

    return result



def create_weixingroup_list():
    result = []
    print("Getting weixin group list...")
    try:
        result = weixin_function.get_group_list().copy()
        print("Successfully get the weixin group list!")
        print("weixin group list:")
        print(result)
    except:
        print("Fail to get the weixin group list! Make sure you have opened Mojoweixin!")
        #sys.exit(-1)

    return result



def isForwardGroup(group_id):
    res = False
    for each_group in forward_group_list:
        if(group_id==each_group[1]):
            res = True
            break
    return res
    


def forwardGroup(inital_group_id, sender, content):
    final_content = '[' + sender + '] ' + content
    #print(len(forward_group_list))
    for each_group in forward_group_list:
        if(each_group[1] != inital_group_id):
            print("Forwarding message to "+str(each_group[0]))
            
            if(isqqGroup(each_group[1])):
                QQ_function.send_group_message(each_group[1],final_content)
            else:
                weixin_function.send_group_message(each_group[1],final_content)
            time.sleep(0.5)
    print("Forwarding message successfully!")
    
    
    
def isqqGroup(group_id):
    res = False
    for each_group in qqgroup_list:
        if(group_id==each_group[1]):
            res = True
            break
    return res
    

def sendGroupList(sender_id):
    QQ_function.send_friend_message(sender_id,group_info)
    

#return forwarded group string
def forwardedGroupstr():
    str_tmp = ""
    for each_group in forward_group_list:
        str_tmp = str_tmp+" "+each_group[0]
    return "(当前连接的群："+str_tmp+")"

def isValidAdd(content):
    if(content.isdigit()):
        content = int(content)
        length = len(all_group_list)
        if(content>=0 and content<length):
            return True
        return False
    else:
        return False
    
    
    
def isValidDelete(content):
    if(content.isdigit()):
        content = int(content)
        length = len(forward_group_list)
        if(content>=0 and content<length):
            return True
        return False
    else:
        return False
    
    
        
def addGroup(content):
    forward_group_list.append(all_group_list[content])
    
    
    
def deleteGroup(content):
    try:
        forward_group_list.remove(all_group_list[content])
    except:
        pass
    
    
    
def isValidGroup(content):
    res = content.split(" ")
    flag = True
    for each_part in res:
        if(not each_part.isdigit()):
            flag=False
            break
        else:
            k = int(each_part)
            if(k<0 or k>=len(all_group_list)):
                flag=False
                break
    return flag



def getGroupsList(content):
    res = content.split(" ")
    return_group = []
    for each_part in res:
        return_group.append(int(each_part))
    return return_group



def sendMassMessage(mass_group,content):
    for each_group in mass_group:
        group_id = all_group_list[each_group][1]
        if(isqqGroup(group_id)):
            QQ_function.send_group_message(group_id,content)
        else:
            weixin_function.send_group_message(group_id,content)
        time.sleep(0.5)
        

        
def send_notification(group_id):
    global current_notification
    if(isqqGroup(group_id)):
        QQ_function.send_group_message(group_id, current_notification)
        time.sleep(0.5)
    else:
        weixin_function.send_group_message(group_id, current_notification)
        time.sleep(0.5)
        
        
def saveRecord(group, sender, content):
    with open(group+"record.txt",'a') as f:
        f.write('['+sender+'] '+content)
        f.write('\n')
        


#need to be reconstruct
def handle_friend_message(sender, sender_id, content):
    global admin
    if(sender != admin):
        return
    return_message = "欢迎使用群聊连接机器人，输入1显示群信息，输入2添加被连接的群，输入3删除被连接的群，输入4群发通知，输入5添加特别关心，输入6删除特别关心"
    
    global state
    global admin_id
    admin_id=sender_id
    #inital state
    if(state==1):
        QQ_function.send_friend_message(sender_id,return_message+forwardedGroupstr())
        state = 2
    #waiting for instructions
    elif(state==2):
        if(content.isdigit()):
            content = int(content)
            #output group list
            if(content==1):
                sendGroupList(sender_id)
            elif(content==2):
                QQ_function.send_friend_message(sender_id,"请输入需要连接的群的序号(输入end取消操作)：")
                state=3
            elif(content==3):
                QQ_function.send_friend_message(sender_id,"请输入需要取消连接的群的序号(输入end取消操作)：")
                state=4
            elif(content==4):
                QQ_function.send_friend_message(sender_id,"请输入需要群发的组序号，序号间用空格隔开(输入end取消操作)：")
                state=5
            elif(content==5):
                QQ_function.send_friend_message(sender_id,"请输入特别关心人的昵称(输入end取消操作)")
                state=7
            elif(content==6):
                QQ_function.send_friend_message(sender_id,"请输入需要删除的特别关心人的昵称(输入end取消操作)")
                state=8
            else:
                QQ_function.send_friend_message(sender_id,"输入非法，请输入正确指令序号")
        else:
            QQ_function.send_friend_message(sender_id,"输入非法，请输入正确指令序号")
    elif(state==3):
        if(content=="end"):
            QQ_function.send_friend_message(sender_id,"已结束当前操作")
            state = 1
        elif(isValidAdd(content)):
            content = int(content)
            addGroup(content)
            QQ_function.send_friend_message(sender_id,"已将群 "+all_group_list[content][0]+" 添加到连接群中")
            state = 1
        else:
            QQ_function.send_friend_message(sender_id,"输入非法，请输入正确指令序号")
    elif(state==4):
        if(content=="end"):
            QQ_function.send_friend_message(sender_id,"已结束当前操作")
            state = 1
        elif(isValidDelete(content)):
            content = int(content)
            deleteGroup(content)
            QQ_function.send_friend_message(sender_id,"已将群 "+all_group_list[content][0]+" 从连接群中删除")
            state = 1
        else:
            QQ_function.send_friend_message(sender_id,"输入非法，请输入正确指令序号")
    elif(state==5):
        if(content=="end"):
            QQ_function.send_friend_message(sender_id,"已结束当前操作")
            state=1
        elif(isValidGroup(content)):
            global mass_group
            mass_group=getGroupsList(content)
            QQ_function.send_friend_message(sender_id,"请输入要群发的内容")
            state=6
        else:
            QQ_function.send_friend_message(sender_id,"输入非法，请输入正确指令序号(输入end取消操作)")
    elif(state==6):
        if(content=="end"):
            QQ_function.send_friend_message(sender_id,"已结束当前操作")
            state=1
        else:
            #global mass_group
            global current_notification
            sendMassMessage(mass_group,content)
            current_notification=content
            QQ_function.send_friend_message(sender_id,"群发成功！")
            state=1
    elif(state==7):
        if(content=="end"):
            QQ_function.send_friend_message(sender_id,"已结束当前操作")
            state=1
        else:
            concerned_people.append(content)
            QQ_function.send_friend_message(sender_id,"已添加"+content+"为特别关心")
            state=1
    elif(content==8):
        if(content=="end"):
            QQ_function.send_friend_message(sender_id,"已结束当前操作")
            state=1
        else:
            try:
                concerned_people.remove(content)
                QQ_function.send_friend_message(sender_id,"已删除"+content+"的特别关心")
            except:
                QQ_function.send_friend_message(sender_id,"特别关心列表无此人，已结束操作")
            state=1
    else:
        pass
            

    

if __name__ == "__main__":
    #get the QQ and weixin group
    qqgroup_list = create_qqgroup_list();
    weixingroup_list = create_weixingroup_list();
    all_group_list = qqgroup_list.copy()
    all_group_list.extend(weixingroup_list)
    
    admin=input("请输入管理员QQ昵称：")
    #group need to be forwarded
    forward_group_list = qqgroup_list.copy()
    
    #create group info string
    num=0
    for each_group in all_group_list:
        group_info = group_info + "[" + str(num)+ "] "+each_group[0]+" "
        num+=1

    #output qq group and weixin group, just for debug
    print("Global qqgroup_list:")
    print(qqgroup_list)
    print("Global weixingroup_list:")
    print(weixingroup_list)
    print("Global forward_group_list:")
    print(forward_group_list)

    #start server, listening on port server_port
    httpd = make_server("127.0.0.1", server_port, application)
    print("Serving http on port "+str(server_port)) 
    httpd.serve_forever()
