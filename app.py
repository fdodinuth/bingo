from flask import Flask, render_template, redirect, url_for, request, jsonify
import random

app = Flask(__name__)

# Store game data
players = []
called_numbers = []
player_tickets = {}
player_tapped_numbers = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_name', methods=['POST'])
def submit_name():
    player_name = request.form['player_name']
    if player_name:
        # Store player name and create their ticket
        players.append(player_name)
        player_ticket = generate_ticket()
        player_tickets[player_name] = player_ticket
        player_tapped_numbers[player_name] = []
        return redirect(url_for('ticket', player_name=player_name))
    return redirect(url_for('index'))

@app.route('/ticket/<player_name>')
def ticket(player_name):
    if player_name not in player_tickets:
        return redirect(url_for('index'))
    ticket = player_tickets[player_name]

    # Create a list of tuples (number, is_called)
    highlighted_ticket = [(number, number in called_numbers) for number in ticket]

    return render_template('ticket.html', player_name=player_name, ticket=ticket, highlighted_ticket=highlighted_ticket)

@app.route('/host')
def host():
    return render_template('host.html', called_numbers=called_numbers, players=player_tapped_numbers)

@app.route('/pick_random', methods=['POST'])
def pick_random():
    # Pick a random number
    number = random.randint(1, 90)
    while number in called_numbers:
        number = random.randint(1, 90)
    called_numbers.append(number)

    # Notify players (check if they have the number)
    players_with_number = []
    for player_name, ticket in player_tickets.items():
        if number in ticket:
            players_with_number.append(player_name)

    # Return the random number and players with it
    return jsonify({'number': number, 'players': players_with_number})

@app.route('/check_called_numbers', methods=['GET'])
def check_called_numbers():
    # Return the list of called numbers as a JSON response
    return jsonify({'called_numbers': called_numbers})


@app.route('/check_number/<player_name>', methods=['POST'])
def check_number(player_name):
    number = request.json['number']

    # Only allow players to tap if the number has been called
    if number not in called_numbers:
        return jsonify({'status': 'not_called', 'message': 'This number has not been called yet'})

    # Update player's ticket if the number is on their ticket
    ticket = player_tickets[player_name]
    if number in ticket and number not in player_tapped_numbers[player_name]:
        # Mark the number as tapped
        player_tapped_numbers[player_name].append(number)
        return jsonify({'status': 'correct', 'ticket': ticket, 'player_name': player_name, 'number': number})

    return jsonify({'status': 'incorrect'})

def generate_ticket():
    # Generate a Bingo ticket with 24 unique random numbers
    numbers = random.sample(range(1, 91), 24)
    return numbers

if __name__ == '__main__':
    app.run(debug=True)
