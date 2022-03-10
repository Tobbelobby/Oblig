#!/usr/bin/env python3
from rich import print
from rich.table import Table
from socket import create_server
from threading import Thread
from champlistloader import load_some_champs
from core import Match, Shape, Team, PairThrow
import pickle
import time


db = []
all_connections = []
player1 = []
player2 = []

sock = create_server(("localhost", 5555))
sock.listen(2)

def db_connection():
    global champions
    conn, address = sock.accept()
    print("We are connected to:", address, "DB")
    champions = conn.recv(2024)
    db.append(conn)
    main()



def main():
    global sock
    global conn
    print("Wating For Players")
    while True:
        conn, address = sock.accept()
        print("We are connected to:", address)
        all_connections.append(conn)
        we = "! WELCOME TO THE GAME !"
        conn.send(we.encode())
        Thread(target = threaded_client).start()


def threaded_client():
    if len(all_connections) != 2:
        time.sleep(3)
    else:
        all_connections[0].send(("red Player 1").encode())
        time.sleep(1)
        all_connections[0].send(champions)
        time.sleep(1)
        all_connections[1].send(("blue Player 2").encode())
        time.sleep(1)
        all_connections[1].send(champions)
        to_players()
 

def to_players():
    p1 = all_connections[0]
    p2 = all_connections[1]
    for _ in range(2):
        the_add(p1 ,player1, player2)
        the_add(p2 ,player2, player1)
    start_match(player1, player2 ,p1 ,p2)


def the_add(player, player1, player2):
    player.send(("DIN").encode())
    time.sleep(0.2)
    e_list = pickle.dumps(player2)
    player.send(e_list)
    while True:
        name = player.recv(2024).decode()
        match name:
            case name if name in player2:
                player.send((f'{name} is in the enemy team. Try again.').encode())
            case _:
                player.send(("OK").encode())
                player1.append(name)
                print("P1 " ,player1)
                print("P2 " ,player2)
                break


def start_match(champions1, champions2, p1, p2):
    champions = load_some_champs()
    match = Match(
        Team([champions[name] for name in champions1]),
        Team([champions[name] for name in champions2]),
    )
    
    
    match.play()
    print_match_summary(match, p1, p2)


def print_match_summary(match: Match, p1, p2) -> None:
    # m_result = pickle.dumps(match.rounds)
    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)
        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        db_round = pickle.dumps(round)
        champions_sending = pickle.dumps(round_summary)
        p1.send(champions_sending)
        p2.send(champions_sending)
        db[0].send(db_round)
        time.sleep(1)
    # Print the score
    red_score, blue_score = match.score
    time.sleep(1)
    p1.send(str(red_score).encode())
    time.sleep(1)
    p1.send(str(blue_score).encode())
    time.sleep(1)
    p2.send(str(red_score).encode())
    time.sleep(1)
    p2.send(str(blue_score).encode())
    time.sleep(1)
    db[0].send(str(red_score).encode())
    time.sleep(1)
    db[0].send(str(blue_score).encode())
    end_clean_up()


def end_clean_up():
    global all_connections
    all_connections.pop(0)
    all_connections.pop(0)
    player1.clear()
    player2.clear()
    print(len(all_connections))
    if len(all_connections) < 2:
        main()
    else:
        threaded_client()

    
if __name__ == "__main__":
    while True:
        db_connection()

