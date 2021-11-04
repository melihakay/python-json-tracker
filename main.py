from datetime import datetime as e, time
import json
import os, time, random
from tabulate import tabulate


ff = "data.json"
file = open(ff, "r+")
active_task_id = ""
largest_id = 0
komut = ""
tag_cont_ids = {}
name_cont_ids = {}
name_tag_list = {}

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
def update(p=False):
    sortsys = 1
    key_list = []
    global largest_id

    for i in data["activity"]:
        key_list.append(i)
    for t in key_list:
        temp = data["activity"][t]
        data["activity"].pop(t)
        data["activity"][sortsys] = temp
        sortsys += 1
    for i in data["activity"]:
        largest_id = int(i)
        tags = data["activity"][i]["tags"]
        for m in tags:
            if not m in tag_cont_ids:
                tag_cont_ids[m] = []
            if not i in tag_cont_ids[m]:
                tag_cont_ids[m].append(i)
    for i in data["activity"]:
        largest_id = int(i)
        name = data["activity"][i]["name"]
        if not name in name_cont_ids:
            name_cont_ids[name] = []
        if not i in name_cont_ids[name]:
            name_cont_ids[name].append(i)
    for i in data["activity"]:
        largest_id = int(i)
        tags = data["activity"][i]["tags"]
        name = data["activity"][i]["name"]
        if not name in name_tag_list:
            name_tag_list[name] = []
        for x in tags:
            if not x in name_tag_list[name]:
                name_tag_list[name].append(x)
    if p: print(tag_cont_ids)
    data["tag_cont_ids"] = tag_cont_ids
    data["name_cont_ids"] = name_cont_ids
    data["name_tag_list"] = name_tag_list
def get_tag():
    tags = []
    while True:
        m = input("Getting tasks each at a time:    ")
        if m == "":
            return tags
        else:
            tags.append(m)
            print("Added tags are:",tags)
def list():
    f_list = []
    for i in reversed(data["activity"]):
        global largest_id
        largest_id = int(i)
        name = data["activity"][i]["name"]
        tags = data["activity"][i]["tags"]
        isActive = data["activity"][i]["active"]
        if isActive == "True":
            activness = "x"
        else: 
            activness = " "
        start_time = data["activity"][i]["start_time"]
        end_time = data["activity"][i]["end_time"]
        dr = duration(start_time,end_time)
        f_list.append([i, activness,name, tags, start_time, end_time, dr[2], dr[1], dr[0]])
        #print("ID = {}, Name = {}, Tags = {}, Duration = {}H {}M {}S".format(i, name, tags, dr[2], dr[1], dr[0]))
    print(tabulate(f_list, headers= ["ID", "A", "Name", "Tags","Start", "End", "Hours", "Minutes", "Seconds"]))
    if tag_cont_ids == {}:
        print("Empty")
def get_time(mes="Get"):
    date = input(f"{mes} Date = ({e.today().strftime('%Y-%m-%d')})    ")
    if date == "":
        date = e.today().strftime('%Y-%m-%d')
    timeget = input(f"{mes} Time = ({e.today().strftime('%H:%M:%S')})    ")
    if timeget == "":
        timeget = e.today().strftime('%H:%M:%S')
    end_str = str(date) + " " + str(timeget)
    return end_str
def duration(start, end=e.now()):
    if type(start) == str:
        start = e.strptime(start, '%Y-%m-%d %H:%M:%S')
    if type(end) == str:
        end = e.strptime(end, '%Y-%m-%d %H:%M:%S')
    if active_task_id:
        if start == e.strptime(activities[active_task_id]["start_time"], '%Y-%m-%d %H:%M:%S'):
            end = e.now()
    duration = end - start
    duration_seconds = duration.total_seconds()
    hours,remainder   = divmod(duration_seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, remainder = divmod(remainder, 1)
    dur_var = (seconds ,minutes, hours, duration_seconds)
    return dur_var
def tracking():
    n = ""
    while not n:
        cls()
        print("Active Task:", activities[active_task_id]["name"],"/", activities[active_task_id]["tags"][0])
        time_passed = duration(activities[active_task_id]["start_time"], e.now())
        print(f"Time passed : {time_passed[0]} seconds", end = " ")
        if time_passed[1]: print(f"{time_passed[1]} minutes", end=" ")
        if time_passed[2]: print(f"{time_passed[2]} hours", end=" ")
        n = input()
file.seek(0,0)
text = file.read()
file.seek(0,0)
if len(text) != 0:
    data = json.load(file)
else:
    data = {"activity" : {}}
activities = data["activity"]

while True:
    while komut != "q":
        update()
        cls()
        for n in data["activity"]:
            if data["activity"][n]["active"] == "True":
                active_task_id = n
                break
            else:
                active_task_id = ""        
        if not active_task_id == "":
            print("Active Task:", activities[active_task_id]["name"],"/", activities[active_task_id]["tags"][0])
        else:
            print("There is no active task.")
        komut = input("Command =    ")
        if komut == "list":
            list()
            input()
        elif komut == "track":
            try: tracking()
            except KeyError: pass
            cls()
        elif komut == "start":
            if active_task_id:
                if input("There is an active task right now which is {}\n Would you like to terminate it and start new one?? (Y)\n     ".format(activities[active_task_id]["name"])) == "y":
                    activities[active_task_id]["active"] = "False"
                    activities[active_task_id]["end_time"] = e.now().strftime('%Y-%m-%d %H:%M:%S')
                else: break
            new_name = input("Name = ")
            if new_name in name_tag_list:
                new_tag = name_tag_list[new_name]
            else:
                new_tag = get_tag()
            new_start = e.now().strftime('%Y-%m-%d %H:%M:%S')
            largest_id += 1
            activities[largest_id] = {"active" : "True", "start_time" : new_start, "end_time" : new_start, "tags" : new_tag , "name" : new_name}
        elif komut == "stop":
            if active_task_id:
                activities[active_task_id]["active"] = "False"
                activities[active_task_id]["end_time"] = e.now().strftime('%Y-%m-%d %H:%M:%S')
                print("Stopped!")
                input()
        elif komut == "add":
            new_name = input("Name = ")
            if new_name in name_tag_list:
                new_tag = name_tag_list[new_name]
            else:
                new_tag = get_tag()
            new_start = get_time("Start")
            new_end = get_time("End")
            largest_id += 1
            activities[largest_id] = {"active" : "False", "start_time" : new_start, "end_time" : new_end, "tags" : new_tag , "name" : new_name}
            print(f"""
            Added past activity as:
                Name: {new_name}
                Tag: {new_tag}
                Start Time: {new_start}
                End Time: {new_end}""")
            input()
        elif komut == "drop":
            id = int(input("ID ?=      "))
            deleted_name = data["activity"][id]["name"]
            try:
                del activities[id]
            except KeyError:
                pass
            print(f"""Deleted {deleted_name}""")
            input()
        elif komut == "ok":
            update()
            data_dump = json.dumps(data,indent=4,default=str)
            file.close()
            file = open("data.json", "w+")
            file.write(data_dump)
            file.close()
            file = open("data.json", "r+")
    break

update()
data_dump = json.dumps(data,indent=4,default=str)
file.close()
file = open("data.json", "w+")
file.write(data_dump)
file.close()
cls()