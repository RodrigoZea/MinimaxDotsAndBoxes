# Cliente totito
# Rodrigo Zea 17058

import socketio
import random
from math import inf as infinity

sio = socketio.Client()

class GameManager:
    def __init__(self):
        self.username = ""
        self.tid = 0
        self.ready = False
        self.boardTiles = []
        self.gameFinished = False
        self.currentGameID = 0
        self.currentTurnID = 0
        self.currentOpponentID = 0
        self.winnerTurnID = 0

vm = GameManager()

def humanBoard(board):
    resultado = ''
    acumulador = 0

    for i in range(int(len(board[0])/5)):
        if board[0][i] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+6] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+12] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+18] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+24] == 99:
            resultado = resultado + '*   *\n'
        else:
            resultado = resultado + '* - *\n'

        if i != 5:
            for j in range(int(len(board[1])/5)):
                if board[1][j + acumulador] == 99:
                    resultado = resultado + '    '
                else:
                    resultado = resultado + '|   '
            acumulador = acumulador + 6
            resultado = resultado + '\n'

    return resultado

def validateMovement(movement):
    
    if movement == []:
        return False
    
    num = None
    for conv in (int, float, complex):
        try:
            num = conv(movement[0])
            break
        except ValueError:
            pass

    if num is None:
        return False

    num = None
    for conv in (int, float, complex):
        try:
            num = conv(movement[1])
            break
        except ValueError:
            pass

    if num is None:
        return False    

    movement = [int(movement[0]), int(movement[1])]

    if movement[0] < 0 or movement[0] > 1:
        return False

    if movement[1] < 0 or movement[1] > 29:
        return False

    return True


@sio.on('connect')
def connect_handler():
    print("Conectado: " + vm.username)

    sio.emit('signin', {
        'user_name': vm.username,
        'tournament_id': vm.tid,
        'user_role': 'player'
    }) 

@sio.on('ready')
def on_ready(data):
    vm.gameFinished = False
    vm.currentGameID = data['game_id']
    vm.currentTurnID = data['player_turn_id']

    if (vm.currentTurnID == 1):
        vm.currentOpponentID = 2
    else:
        vm.currentOpponentID = 1

    vm.boardTiles = data['board']

    vm.ready = True

    movement = []

    print(humanBoard(data['board']))

    while validateMovement(movement) != True:
        # 0 or 1 to represent the array to modify
        # 0: horizontal
        # 1: vertical
        #direction = int(input("Direction to modify: "))
        direction = random.randint(0, 1)

        # Number between 0 a 29
        #position = int(input("Slot to modifiy: "))
        position = random.randint(0, 29)

        movement = [direction, position]
        print("Movement played: " + str(movement[0]) + ", " + str(movement[1]))

    sio.emit('play', {
        'tournament_id': vm.tid,
        'player_turn_id': vm.currentTurnID,
        'game_id': vm.currentGameID,
        'movement': movement
    })

@sio.on('finish')
def on_finish(data):
    vm.currentGameID = data['game_id']
    vm.currentTurnID = data['player_turn_id']
    vm.winnerTurnID = data['winner_turn_id']

    print('Game finished!')
    vm.gameFinished = True

    print('Ready again.')
    sio.emit('player_ready', {
        'tournament_id': vm.tid,
        'game_id': vm.currentGameID,
        'player_turn_id': data['player_turn_id']
    })

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")


def main():
    n = 30
    coordinatorHost = input("Coordinator fully qualified host and port: ")
    vm.tid = int(input("Tournament ID: "))
    vm.username = input("Username: ")

    sio.connect(coordinatorHost)

    vm.ready = False
    vm.winnerTurnID = 0


main()