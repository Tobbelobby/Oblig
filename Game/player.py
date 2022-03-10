#!/usr/bin/env python3
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from socket import create_connection
from champlistloader import load_some_champs
from core import Champion
import pickle, sys

player1 = []
player2 = []

PLAYER = None
COLOR = None


def start():
    global sock
    global PLAYER
    global COLOR
    global champions
    sock = create_connection(("localhost", 5555))
    from_server = sock.recv(1024).decode()
    print(from_server)
    while True:
        play_num = sock.recv(2024).decode()
        if play_num:
            temp = play_num.split()
            PLAYER = temp[1:]
            COLOR = temp[0]
            PLAYER = (PLAYER[0] + " " + PLAYER[1])
            print(PLAYER)
            print(COLOR)
            champions = sock.recv(2024)
            champions = pickle.loads(champions)
            print_available_champs(champions)
            break



def wating_room():
    if len((player1)) == 2:
        match_result()    
    turn = sock.recv(2024).decode()
    if turn == "DIN":
        picking_up_teammates()

# from team-...-..-.. to pretty print()
def print_available_champs(champions: dict[Champion]) -> None:
    
            
    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)
    print(available_champs)
    wating_room()

def picking_up_teammates():
    while True:
        input_champion(PLAYER, COLOR,champions, player1, player2,)
        if len(player1) == 2:
            wating_room()
            break
    print('\n')


def input_champion(prompt: str,
                   color: str,
                   champions,
                   player1,
                   player2) -> None:

    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    e_list = sock.recv(2024)
    e_list = pickle.loads(e_list)
    print(f"The enemy team {e_list}")
    while True:
        name = Prompt.ask(f'[{color}]{prompt}')
        if name in player1:
            print(f'{name} is already in your team. Try again.')
        elif name not in champions:
            print(f'The champion {name} is not available. Try again.')
        elif name in player1:
            print(f'{name} is already in your team. Try again.')
        else:
            sock.send((name).encode())
            is_ok = sock.recv(2024).decode()
            print(is_ok)
            if is_ok == "OK":
                player1.append(name)
                wating_room()
                break
              
def match_result():
    for _ in range(3):
        round_1 = sock.recv(2024)
        round_1 = pickle.loads(round_1)
        print(round_1)
        print(" ")
    result()


def result():
    red_score = sock.recv(2024).decode()
    blue_score = sock.recv(2024).decode()
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')
        # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')
    sys.exit()


start()
