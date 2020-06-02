# Cliente totito
# Rodrigo Zea 17058

import socketio
import random
import numpy as np
from math import inf as infinity

sio = socketio.Client()

class GameManager:
    def __init__(self):
        self.username = ""
        self.tid = 0
        self.ready = False
        self.boardTiles = []
        self.originalBoard = []
        self.gameFinished = False
        self.currentGameID = 0
        self.currentTurnID = 0
        self.currentOpponentID = 0
        self.winnerTurnID = 0

vm = GameManager()

def ingresarPuntos(oldBoard, move, playerNumber):
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6

    board = list(map(list, oldBoard))

    punteoInicial = 0
    punteoFinal = 0

    acumulador = 0
    contador = 0
    multiplicador = 0

    if (playerNumber == vm.currentTurnID):
        multiplicador = 1
    else:
        multiplicador = -1

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoInicial = punteoInicial + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0

    board[move[0]][move[1]] = FILL

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoFinal = punteoFinal + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    
    if punteoInicial < punteoFinal:
        if playerNumber == 1:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP12
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP11
        elif playerNumber == 2:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP22
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP21

    return (punteoFinal - punteoInicial)*multiplicador

def doMove(oldBoard, move, playerNumber):
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6

    board = list(map(list, oldBoard))

    punteoInicial = 0
    punteoFinal = 0

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoInicial = punteoInicial + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0

    board[move[0]][move[1]] = FILL

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoFinal = punteoFinal + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    
    if punteoInicial < punteoFinal:
        if playerNumber == 1:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP12
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP11
        elif playerNumber == 2:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP22
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP21
    
    return board

def getPossibleMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if int(board[i][j]) == 99:
                moves.append((i, j))

    return moves

def minimax_full(board, pos, depth, alpha, beta, maxPlayer):
    idCheck = vm.currentTurnID if maxPlayer else vm.currentOpponentID

    if depth == 0 or 99 not in np.asarray(board).reshape(-1):
        return ingresarPuntos(board, pos, idCheck)

    possibleMoves = getPossibleMoves(board)

    # Max
    if (maxPlayer):
        maxEval = -infinity
        # Recorrer lista de posibles movimientos
        for move in possibleMoves:
            # Hacer movimiento
            board = doMove(board, move, idCheck)
            # Evaluar
            eval = minimax_full(board, move, depth - 1, alpha, beta, False)
            # Deshacer movimiento
            board[move[0]][move[1]] = 99
            # Nodo max
            maxEval = max(maxEval, eval)
            # Guardar alpha
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return maxEval
    # Min
    else:
        minEval = infinity
        # Recorrer lista de posibles movimientos
        for move in possibleMoves:
            # Hacer movimiento
            board = doMove(board, move, idCheck)
            # Evaluar
            eval = minimax_full(board, move, depth - 1, alpha, beta, True)
            # Deshacer movimiento
            board[move[0]][move[1]] = 99
            # Nodo min
            minEval = min(minEval, eval)
            # Guardar beta
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return minEval

def bestMove(board):
    bestScore = -infinity
    for i in range(0,2):
            for j in range(0, 30):
                if board[i][j] == 99:
                    board[i][j] = vm.currentTurnID
                    score = minimax_full(board, (i, j), 3, -infinity, infinity, False)
                    board[i][j] = 99
                    if (score > bestScore):
                        bestScore = score
                        move = (i, j)

    return move

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
    vm.originalBoard = data['board']

    vm.ready = True

    movement = []

    print(humanBoard(data['board']))

    while validateMovement(movement) != True:
        move = bestMove(vm.boardTiles)
    
        movement = [move[0], move[1]]
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

    if data['player_turn_id'] == data['winner_turn_id']:
        print("Ganaste :D")
    else:
        print("Perdiste :(")

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
    coordinatorHost = input("Coordinator fully qualified host and port: ")
    vm.tid = int(input("Tournament ID: "))
    vm.username = input("Username: ")

    sio.connect(coordinatorHost)

    vm.ready = False
    vm.winnerTurnID = 0

main()