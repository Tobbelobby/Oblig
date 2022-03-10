#!/usr/bin/env python3

from rich import print
from socket import create_connection
from champlistloader import load_some_champs
import pickle,json,re 
from datetime import datetime

# For safe keeping
save = { "CHAMPIONS":
    {
        "Vain":0,
        "Dr. Yi":0,
        "Twist":0,
        "Guan":0,
        "Siva":0,
        "Katina":0,
        "Asir":0,
        "Cactus":0,
        "Luanne":0,
    },
        'MATCH':[],

    'OVERALL': {'RED': 0, 'BLUE': 0, 'DRAW': 0}
}


with open('db.json', 'r') as f:
        data_save = json.load(f)

def filter_sending():
    data = data_save["MATCH"][-1]
    for r in range(1,4):
        filter_data(data[r])

# Filtering the to ["name","name","ROCK","PAPER","name",.....]
def filter_data(data):
    data = data.replace("PairThrow","")
    data = data.replace(": (red=<Shape", "")
    data = data.replace("blue=<Shape", "")
    data = re.sub(" \d+", " ", data)
    data = re.sub('[^\w]', ' ', data)
    data = data.split()
    match1_team = data[0:2]
    par = data[2:4]
    match2_team = data[4:6]
    par2 = data[6:8]
    adder(par,match1_team)
    adder(par2,match2_team)


# Game logic 
def adder(par,team):
    ch = par[0]
    mot = par[1]
    if ch == "ROCK":
        if mot == "SCISSORS":
            i = par.index("ROCK")
            name = team[i]
            data_save["CHAMPIONS"][name] += 1
        else:
            i = par.index("PAPER")        
            name = team[i]
            data_save["CHAMPIONS"][name] += 1
    elif ch == "PAPER":
        if mot == "ROCK":
            i = par.index("PAPER")
            name = team[i]
            data_save["CHAMPIONS"][name] += 1
        else:
            i = par.index("SCISSORS")
            name = team[i]
            data_save["CHAMPIONS"][name] += 1
    elif ch == "SCISSORS":
        if mot == "PAPER":
            i = par.index("SCISSORS")
            name = team[i]
            data_save["CHAMPIONS"][name] += 1
        else:
            i = par.index("ROCK")
            name = team[i]
            data_save["CHAMPIONS"][name] += 1

# adding to the json file 
def match_result():
    champions = load_some_champs()
    champions = pickle.dumps(champions)
    sock.send(champions)
    m = []
    match_time = datetime.now()
    m.append(str(match_time))
    for _ in range(3):
        round_1 = sock.recv(2024)
        round_1 = pickle.loads(round_1)
        m.append(str(round_1))

    red_score = sock.recv(2024).decode()
    blue_score = sock.recv(2024).decode()
    m.append(red_score)
    m.append(blue_score)
    if red_score > blue_score:
        data_save["OVERALL"]["RED"] += 1
    elif blue_score > red_score:
        data_save["OVERALL"]["BLUE"] += 1
    else:
        data_save["OVERALL"]["DRAW"] += 1

    data_save["MATCH"].append(m)
    filter_sending()
    print(json.dumps(data_save, sort_keys=True, indent=4))
    save_to_json()

def save_to_json():
    with open('db.json', 'w') as data:
        data.write(json.dumps(data_save, indent=4, sort_keys=True))


if __name__ == "__main__":
    sock = create_connection(("localhost", 5555))
    while True:
        match_result()



