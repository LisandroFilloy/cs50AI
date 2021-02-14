from tictactoe import initial_state, result, actions, winner, terminal, utility, minimax, minPlay

x = initial_state()

while(not terminal(x)):
	print(minimax(x))
	x = result(x, minimax(x))




