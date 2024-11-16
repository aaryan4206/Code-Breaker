let score = 0;
let round = 1;
let questionTimer;
let timePerQuestion = 120; // Initial time for the first round
let allTimeHighScore = 0;

function startGame() {
    document.getElementById('start-screen').style.display = 'none';
    document.getElementById('game-screen').style.display = 'block';
    score = 0; // Reset score
    round = 1; // Reset round
    timePerQuestion = 120; // Reset time for questions
    document.getElementById('score').innerText = `Score: ${score}`;
    document.getElementById('round').innerText = `Round: ${round}`;
    resetTimer();
    fetchQuestion();
}

function fetchQuestion() {
    clearInterval(questionTimer);
    resetTimer();
    fetch('/get_question')
        .then(response => response.json())
        .then(data => {
            if (data.round_completed) {
                nextRound();
            } else {
                displayQuestion(data);
            }
        })
        .catch(error => console.error('Error fetching question:', error));
}

function displayQuestion(data) {
    document.getElementById('question').innerText = data.question;
    document.getElementById('points').innerText = `Points: ${data.points}`;
    document.getElementById('answer').value = '';
    startTimer(timePerQuestion);
}

function submitAnswer() {
    const answer = document.getElementById('answer').value;

    fetch('/check_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answer }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.correct) {
                score = data.new_score;
                document.getElementById('score').innerText = `Score: ${score}`;
                document.getElementById('correct-audio').play()
            }
            else{
                document.getElementById('incorrect-audio').play()
            }
            fetchQuestion();
        })
        .catch(error => console.error('Error checking answer:', error));
}

function startTimer(duration) {
    let timeRemaining = duration;
    document.getElementById('timer').innerText = `Time Left: ${timeRemaining}s`;

    questionTimer = setInterval(() => {
        timeRemaining--;
        document.getElementById('timer').innerText = `Time Left: ${timeRemaining}s`;

        if (timeRemaining <= 0) {
            clearInterval(questionTimer);
            alert('Time is up! Moving to the next question.');
            fetchQuestion();
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(questionTimer);
}

function nextRound() {
    round++;
    if (timePerQuestion > 20) {
        timePerQuestion -= 10; // Decrease time by 10 seconds per round
    }
    document.getElementById('round').innerText = `Round: ${round}`;
    fetch('/next_round', { method: 'POST' })
        .then(() => {
            fetchQuestion();
        })
        .catch(error => console.error('Error proceeding to the next round:', error));
}

function toggleMenu() {
    const menu = document.getElementById('menu');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

function restartGame() {
    score = 0;
    round = 1;
    timePerQuestion = 120; // Reset the timer for the first round
    document.getElementById('score').innerText = `Score: ${score}`;
    document.getElementById('round').innerText = `Round: ${round}`;
    fetch('/restart', { method: 'POST' })
        .then(() => {
            fetchQuestion();
        })
        .catch(error => console.error('Error restarting game:', error));
}

function endGame() {
    fetch('/end_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.new_high_score) {
                alert(`Congratulations! You've set a new high score: ${score}`);
                allTimeHighScore = score;
            }
            window.location.reload();
        })
        .catch(error => console.error('Error ending game:', error));
}
