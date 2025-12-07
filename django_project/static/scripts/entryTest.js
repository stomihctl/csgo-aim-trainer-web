const questions = [
    {
        type: "single",
        text: "Which grenade is used to temporarily blind enemies?",
        options: ["Flashbang", "Smoke", "Molotov", "HE Grenade"],
        answer: [0]
    },
    {
        type: "multi",
        text: "Which of the following factors affect aiming accuracy?",
        options: ["Movement", "Weapon type", "Time of day", "Recoil"],
        answer: [0, 1, 3]
    },
    {
        type: "info",
        text: "How many hours per week do you play CS2?",
        options: ["Less than 5 hours", "5-10 hours", "10-20 hours", "More than 20 hours"],
        answer: null
    },
    {
        type: "reflex",
        text: "Click the targets as fast as you can! You have 10 seconds.",
        answer: null
    }
];

let currentQuestion = 0;
let score = 0;
let reflexClicks = 0;
let gameInterval = null;
let spawnInterval = null;

function loadQuestion() {
    const area = document.getElementById("test-area");
    const game = document.getElementById("reflex-game");
    const q = questions[currentQuestion];
    area.innerHTML = `<div class="question">${q.text}</div>`;
    game.style.display = "none";
    game.innerHTML = "";

    if (q.type === "single") {
        q.options.forEach((opt, i) => {
            area.innerHTML += `<label><input type="radio" name="q${currentQuestion}" value="${i}"> ${opt}</label>`;
        });
    } else if (q.type === "multi") {
        q.options.forEach((opt, i) => {
            area.innerHTML += `<label><input type="checkbox" name="q${currentQuestion}" value="${i}"> ${opt}</label>`;
        });
    } else if (q.type === "info") {
        q.options.forEach((opt, i) => {
            area.innerHTML += `<label><input type="radio" name="q${currentQuestion}" value="${i}"> ${opt}</label>`;
        });
    } else if (q.type === "reflex") {
        area.innerHTML = `<div class="question">${q.text}</div>`;
        startReflexGame();
    }
}

function nextQuestion() {
    const q = questions[currentQuestion];
    if (q.type === "single") {
        const selected = document.querySelector(`input[name="q${currentQuestion}"]:checked`);
        if (selected && parseInt(selected.value) === q.answer[0]) {
            score++;
        }
    } else if (q.type === "multi") {
        const selected = Array.from(document.querySelectorAll(`input[name="q${currentQuestion}"]:checked`))
                              .map(el => parseInt(el.value)).sort();
        if (JSON.stringify(selected) === JSON.stringify(q.answer)) {
            score++;
        }
    } else if (q.type === "reflex") {
        score += Math.min(reflexClicks, 10); // Cap reflex contribution
    }

    currentQuestion++;
    if (currentQuestion < questions.length) {
        loadQuestion();
    } else {
        showResults();
    }
}

function startReflexGame() {
    const game = document.getElementById("reflex-game");
    game.style.display = "block";
    reflexClicks = 0;
    let timeLeft = 10;

    if (gameInterval) clearInterval(gameInterval);
    if (spawnInterval) clearInterval(spawnInterval);

    spawnInterval = setInterval(spawnTarget, 700);

    gameInterval = setTimeout(() => {
        clearInterval(spawnInterval);
        game.innerHTML = "";
        document.getElementById("next-btn").disabled = false;
        alert("Time's up! You clicked " + reflexClicks + " targets.");
    }, timeLeft * 1000);

    document.getElementById("next-btn").disabled = true;
}

function spawnTarget() {
    const game = document.getElementById("reflex-game");
    const target = document.createElement("div");
    target.classList.add("target");
    target.style.top = Math.random() * (game.clientHeight - 30) + "px";
    target.style.left = Math.random() * (game.clientWidth - 30) + "px";

    target.addEventListener("click", () => {
        reflexClicks++;
        target.remove();
    });

    game.appendChild(target);

    setTimeout(() => {
        if (target.parentNode) target.remove();
    }, 800);
}

function showResults() {
    document.getElementById("test-area").innerHTML = "";
    document.getElementById("reflex-game").style.display = "none";
    document.getElementById("next-btn").style.display = "none";
    document.getElementById("result").innerHTML = `
        <strong>Test complete!</strong><br>
        Your total score: ${score}<br>
        Reflex clicks: ${reflexClicks}
    `;

    // Submit results to the server
    document.getElementById("score-input").value = score;
    document.getElementById("reflex-input").value = reflexClicks;
    document.getElementById("entry-test-form").submit();
}

window.onload = loadQuestion;