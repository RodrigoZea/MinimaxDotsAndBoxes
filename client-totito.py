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

# Gracias a David Soto por la heuristica
""" EVERYTHING POINT RELATED """
def addPoints(oldBoard, move, playerNumber):
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6

    #print(str(playerNumber))

    board = list(map(list, oldBoard))

    punteoInicial = 0
    punteoFinal = 0

    acumulador = 0
    contador = 0
    multiplicador = 0

    if (playerNumber == vm.currentTurnID):
        multiplicador = -1
    else:
        multiplicador = 1

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

    #print(str(playerNumber))

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

""" MINIMAX """
# Max
def max_m(tboard, movement, depth, alpha, beta):
    possibleMoves = getPossibleMoves(tboard)
    maxEval = -infinity

    # Recorrer lista de posibles movimientos
		for movement in possibleMoves:
			# Evaluar
			eval = minimax_full(tboard, movement, depth - 1, alpha, beta, False)
            # Nodo max
			maxEval = max(maxEval, eval)
			# Guardar alpha para acelerar procesos
			alpha = max(alpha, eval)

			if beta <= alpha:
				break

    # Deshacer movimiento
	tboard[movement[0]][movement[1]] = 99

    return maxEval

#Min
def min_m(tboard, movement, depth, alpha, beta):
    possibleMoves = getPossibleMoves(tboard)
    minEval = infinity

		# Recorrer lista de posibles movimientos
		for movement in possibleMoves:
			# Evaluar
			eval = minimax_full(tboard, movement, depth - 1, alpha, beta, True)
			# Nodo min
			minEval = min(minEval, eval)
			# Guardar beta para acelerar procesos
			beta = min(beta, eval)
			if beta <= alpha:
				break

	# Deshacer movimiento
	tboard[movement[0]][movement[1]] = 99

    return minEval

def minimax_full(originalBoard, movement, depth, alpha, beta, maxPlayer):
	idCheck = vm.currentTurnID if maxPlayer else vm.currentOpponentID
	score = addPoints(originalBoard, movement, idCheck)

	if depth == 0 or score != 0 or 99 not in np.asarray(originalBoard).reshape(-1):
		return addPoints(originalBoard, movement, idCheck)

    # Hacer movimiento
	tboard = doMove(originalBoard, movement, idCheck)
	
    # Main minimax
    # Si es el caso, maximizar al jugador
	if maxPlayer:
		return max_m(tboard, movement, depth, alpha, beta)
	# Si no, minimizar al oponente
    else:
		return min_m(tboard, movement, depth, alpha, beta)

""" UTILITIES """
def getPossibleMoves(board):
	movements = []

	for i in range(len(board)):
		for j in range(len(board[0])):
			if int(board[i][j]) == 99:
				movements.append((i, j))

	return movements

def optimize():
	wscore = 2 * (99 * 30) 
	tscore = (99 * 30) + (99 * (30 - 1)) #89001 
	return [wscore, tscore]

def bestMove(board):
	best_score = -infinity
	op_moves = []

	moves = getPossibleMoves(board)
	t_score = int(np.sum(board))
		 
	if t_score in optimize():
		return moves[0]
	else:
		for move in moves:
			score = minimax_full(board, move, 1, -infinity, infinity, False)

			if score > best_score:
				best_score = score
				moves = []

			if score >= best_score:
				moves.append(move)

	return random.choice(moves)

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
    vm.currentGameID = data['game_id']
    vm.currentTurnID = data['player_turn_id']
    vm.boardTiles = data['board']
    vm.originalBoard = data['board']

    if(data['player_turn_id'] == 1):
        vm.currentTurnID = data['player_turn_id']
        vm.currentOpponentID = 2
    else:
        vm.currentTurnID = data['player_turn_id']
        vm.currentOpponentID = 1

    print(humanBoard(data['board']))
    movement = bestMove(vm.boardTiles)
    
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
        print("Ganaste")
    else:
        print("Perdiste")

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