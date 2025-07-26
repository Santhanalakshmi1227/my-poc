from flask import Flask, request, jsonify

app = Flask(__name__)


game_state = {
    "board_size": 3,
    "board": [],
    "player_turn": "PlayerX",
    "game_on": False,
    "winner": None
}
def toggle_player(p): 
    return "PlayerY" if p == "PlayerX" else "PlayerX"

def check_win(board, size):
    wins = []

    for r in range(size):
        wins.append([r * size + c for c in range(size)]) 
    for c in range(size):
        wins.append([r * size + c for r in range(size)]) 
    wins.append([i * (size + 1) for i in range(size)])    
    wins.append([(i + 1) * (size - 1) for i in range(size)])  

    for combo in wins:
        line = [board[i] for i in combo]
        if line.count('X') == size or line.count('O') == size:
            return True
    return False




@app.route('/api/health', methods=['GET'])
def ping():
    return jsonify({"status": "OK"})



@app.route('/api/game_state/start', methods=['POST'])
def start_game():
    size = request.json.get("size", 3)
    if not isinstance(size, int) or size < 3:
        return jsonify({"error": "Invalid board size"}), 400

    game_state["board_size"] = size
    game_state["board"] = [''] * (size * size)
    game_state["player_turn"] = "PlayerX"
    game_state["game_on"] = True
    game_state["winner"] = None

    return jsonify({"message": f"{size}x{size} game started", "board": game_state["board"], "player": "PlayerX"})

@app.route('/api/game_state/move', methods=['POST'])
def make_move():
    if not game_state["game_on"]:
        return jsonify({"error": "Game not started or already ended"}), 400

    position = request.json.get("position")
    if not isinstance(position, int) or not (1 <= position <= game_state["board_size"]**2):
        return jsonify({"error": "Invalid position"}), 400

    index = position - 1
    if game_state["board"][index] != '':
        return jsonify({"error": "Cell already taken"}), 400

    symbol = 'X' if game_state["player_turn"] == "PlayerX" else 'O'
    game_state["board"][index] = symbol

    if check_win(game_state["board"], game_state["board_size"]):
        game_state["game_on"] = False
        game_state["winner"] = game_state["player_turn"]
        return jsonify({
            "board": game_state["board"],
            "message": f"{game_state['player_turn']} wins!",
            "winner": game_state["winner"]
        })

    elif '' not in game_state["board"]:
        game_state["game_on"] = False
        return jsonify({
            "board": game_state["board"],
            "message": "It's a draw!",
            "winner": "Draw"
        })

    game_state["player_turn"] = toggle_player(game_state["player_turn"])

    return jsonify({
        "board": game_state["board"],
        "next_player": game_state["player_turn"],
        "message": "Move accepted"
    })


@app.route('/api/game_state/state', methods=['GET'])
def get_state():
    return jsonify(game_state)


@app.route('/api/game_state/reset', methods=['POST'])
def reset_game():
    game_state.update({
        "board_size": 3,
        "board": [],
        "player_turn": "PlayerX",
        "game_on": False,
        "winner": None
    })
    return jsonify({"message": "Game reset."})

if __name__ == '__main__':
    app.run(debug=True)
