from flask import Flask, jsonify, request, render_template, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----'
}


# Simple Caesar Cipher encryption function
def caesar_encrypt(text, shift):
    encrypted_word = []

    for char in text:
        if char.isalpha():  # Check if the character is a letter
            start = ord('A') if char.isupper() else ord('a')  # Determine ASCII start
            shifted = (ord(char) - start + shift) % 26 + start  # Perform the shift
            encrypted_word.append(chr(shifted))
        else:
            encrypted_word.append(char)  # Non-alphabetic characters are not shifted

    return ''.join(encrypted_word)


# Convert text to binary
def text_to_binary(text):
    return ' '.join(format(ord(x), '08b') for x in text)


questions = [
    {"question": "What is the binary of 'A'?", "answer": text_to_binary('A'), "points": 10},
    {"question": "Translate 'HELLO' to Morse Code.", "answer": ".... . .-.. .-.. ---", "points": 10},
    {"question": "Caesar Cipher of 'DOG' with shift 3?", "answer": caesar_encrypt("DOG", 3), "points": 10},
    {"question": "What is the binary of 'B'?", "answer": text_to_binary('B'), "points": 10},
    {"question": "Translate 'E' to Morse Code.", "answer": ".", "points": 10},
    {"question": "Caesar Cipher of 'CAT' with shift 4?", "answer": caesar_encrypt("CAT", 4), "points": 10},
    {"question": "What is the binary of 'C'?", "answer": text_to_binary('C'), "points": 10},
    {"question": "Translate 'HI' to Morse Code.", "answer": ".... ..", "points": 10},
    {"question": "Caesar Cipher of 'BAT' with shift 2?", "answer": caesar_encrypt("BAT", 2), "points": 10},
    {"question": "What is the binary of 'D'?", "answer": text_to_binary('D'), "points": 10},

    # Medium questions
    {"question": "What is the binary of 'HELLO'?", "answer": text_to_binary('HELLO'), "points": 20},
    {"question": "Translate 'SOS' to Morse Code.", "answer": "... --- ...", "points": 20},
    {"question": "Caesar Cipher of 'WORLD' with shift 5?", "answer": caesar_encrypt("WORLD", 5), "points": 20},
    {"question": "What is the binary of 'PYTHON'?", "answer": text_to_binary('PYTHON'), "points": 20},
    {"question": "Translate 'CODE' to Morse Code.", "answer": "-.-. --- -.. .", "points": 20},
    {"question": "Caesar Cipher of 'SECRET' with shift 7?", "answer": caesar_encrypt("SECRET", 7), "points": 20},
    {"question": "What is the binary of 'ALPHA'?", "answer": text_to_binary('ALPHA'), "points": 20},
    {"question": "Translate 'RUN' to Morse Code.", "answer": ".-. ..- -.", "points": 20},
    {"question": "Caesar Cipher of 'HACK' with shift 9?", "answer": caesar_encrypt("HACK", 9), "points": 20},
    {"question": "What is the binary of 'OMEGA'?", "answer": text_to_binary('OMEGA'), "points": 20},

    # Hard questions
    {"question": "What is the binary of 'CRYPTO'?", "answer": text_to_binary('CRYPTO'), "points": 30},
    {"question": "Translate 'DATA' to Morse Code.", "answer": "-.. .- - .-", "points": 30},
    {"question": "Caesar Cipher of 'ENCRYPT' with shift 12?", "answer": caesar_encrypt("ENCRYPT", 12), "points": 30},
    {"question": "What is the binary of 'KNOWLEDGE'?", "answer": text_to_binary('KNOWLEDGE'), "points": 30},
    {"question": "Translate 'SECURE' to Morse Code.", "answer": "... . -.-. ..- .-. .", "points": 30},
    {"question": "Caesar Cipher of 'ALGORITHM' with shift 8?", "answer": caesar_encrypt("ALGORITHM", 8), "points": 30},
    {"question": "What is the binary of 'CYBER'?", "answer": text_to_binary('CYBER'), "points": 30},
    {"question": "Translate 'PROTECT' to Morse Code.", "answer": ".--. .-. --- - . -.-. -", "points": 30},
    {"question": "Caesar Cipher of 'INFORMATION' with shift 3?", "answer": caesar_encrypt("INFORMATION", 3),
     "points": 30},
    {"question": "What is the binary of 'SECURITY'?", "answer": text_to_binary('SECURITY'), "points": 30},

    # Bonus questions
    {"question": "Bonus: Binary of 'COMPUTER'?", "answer": text_to_binary('COMPUTER'), "points": 50},
    {"question": "Bonus: Caesar Cipher of 'NETWORK' with shift 14?", "answer": caesar_encrypt("NETWORK", 14),
     "points": 50},
    {"question": "Bonus: Binary of 'ENGINEERING'?", "answer": text_to_binary('ENGINEERING'), "points": 50},
    {"question": "Bonus: Morse Code for 'HELP'", "answer": ".... . .-.. .--.", "points": 50},
    {"question": "Bonus: Caesar Cipher of 'SOFTWARE' with shift 10?", "answer": caesar_encrypt("SOFTWARE", 10),
     "points": 50},

    # Additional questions
    {"question": "What is the binary of 'HARDWARE'?", "answer": text_to_binary('HARDWARE'), "points": 10},
    {"question": "Translate 'SCIENCE' to Morse Code.", "answer": "... -.-. .. . -. -.-.", "points": 10},
    {"question": "Caesar Cipher of 'TECHNOLOGY' with shift 6?", "answer": caesar_encrypt("TECHNOLOGY", 6),
     "points": 10},
    {"question": "Binary of 'PROGRAMMING'?", "answer": text_to_binary('PROGRAMMING'), "points": 10},
    {"question": "Translate 'DEBUG' to Morse Code.", "answer": "-.. . -... ..- --.", "points": 10},
    {"question": "Caesar Cipher of 'LANGUAGE' with shift 5?", "answer": caesar_encrypt("LANGUAGE", 5), "points": 10},
    {"question": "Binary of 'PYTHON'?", "answer": text_to_binary('PYTHON'), "points": 10},
    {"question": "Morse Code for 'SKILLS'", "answer": "... -.- .. .-.. .-.. ...", "points": 10},
    {"question": "Caesar Cipher of 'PYTHON' with shift 13?", "answer": caesar_encrypt("PYTHON", 13), "points": 10},
    {"question": "Binary of 'LEARN'", "answer": text_to_binary('LEARN'), "points": 10}
]

used_questions = []
high_score = 0
current_score = 0
round_count = 1
questions_per_round = 5
time_per_question = 120  # Initial time per question


@app.route('/')
def start_screen():
    return render_template('index.html', high_score=high_score)


@app.route('/get_question', methods=['GET'])
def get_question():
    global used_questions, round_count, questions_per_round, time_per_question

    remaining_questions = [q for q in questions if q not in used_questions]
    if not remaining_questions:
        return jsonify({"error": "No more questions available."})

    if len(used_questions) >= round_count * questions_per_round:
        return jsonify({"round_completed": True})

    question = random.choice(remaining_questions)
    used_questions.append(question)
    return jsonify({
        "question": question["question"],
        "points": question["points"],
        "time": time_per_question
    })


@app.route('/check_answer', methods=['POST'])
def check_answer():
    global current_score
    data = request.get_json()
    user_answer = data.get("answer", "").strip().lower()

    if not used_questions:
        return jsonify({"error": "No active question to check."})

    current_question = used_questions[-1]
    correct_answer = current_question["answer"]

    if user_answer == correct_answer.lower():
        current_score += current_question["points"]
        return jsonify({"correct": True, "points": current_question["points"], "new_score": current_score})
    else:
        return jsonify({"correct": False, "points": 0, "new_score": current_score})


@app.route('/restart', methods=['POST'])
def restart_game():
    global current_score, round_count, questions_per_round, time_per_question, used_questions
    # Reset game session variables
    used_questions = []
    round_count = 1
    current_score = 0
    questions_per_round = 5
    time_per_question = 120
    session['score'] = 0
    session['round'] = 1
    session['questions_asked'] = []  # Reset the list of asked questions
    return jsonify({'message': 'Game restarted successfully'})


@app.route('/end_game', methods=['POST'])
def end_game():
    global high_score
    score = request.json.get('score', 0)
    new_high_score = False

    if score > high_score:
        high_score = score
        new_high_score = True

    global current_score, round_count, questions_per_round, time_per_question, used_questions
    # Reset game session variables
    used_questions = []
    round_count = 1
    current_score = 0
    questions_per_round = 5
    time_per_question = 120
    session['score'] = 0
    session['round'] = 1
    session['questions_asked'] = []

    return jsonify({'new_high_score': new_high_score, 'high_score': high_score})


@app.route('/next_round', methods=['POST'])
def next_round():
    global round_count, time_per_question
    round_count += 1
    time_per_question = max(20, time_per_question - 10)  # Decrease time but ensure a minimum of 10 seconds
    return jsonify({"message": "Next round started.", "round": round_count, "time": time_per_question})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
