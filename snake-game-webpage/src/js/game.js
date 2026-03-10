// Game Constants
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const box = 20;

// Game Variables
let game;
let gameStarted = false;
let snake = [];
let food;
let d;
let score;

const playerName = localStorage.getItem("currentPlayer") || "Unknown Player";

function initializeGame() {
  document.getElementById("playerNameDisplay").innerText = playerName;
  snake = [];
  snake[0] = {
    x: Math.floor(canvas.width / box / 2) * box,
    y: Math.floor(canvas.height / box / 2) * box,
  };
  d = null; // Initial direction is null
  score = 0;
  gameStarted = false;
  placeFood();
  drawInitialScreen();
}

function placeFood() {
  food = {
    x: Math.floor(Math.random() * Math.floor(canvas.width / box)) * box,
    y: Math.floor(Math.random() * Math.floor(canvas.height / box)) * box,
  };
}

document.addEventListener("keydown", function (event) {
  if (!gameStarted) {
    // Start game on first arrow key press
    gameStarted = true;
    d = d || "RIGHT"; // Default initial direction
    game = setInterval(draw, 100);
  }
  if (event.keyCode == 37 && d != "RIGHT") {
    d = "LEFT";
  } else if (event.keyCode == 38 && d != "DOWN") {
    d = "UP";
  } else if (event.keyCode == 39 && d != "LEFT") {
    d = "RIGHT";
  } else if (event.keyCode == 40 && d != "UP") {
    d = "DOWN";
  }
});

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw snake
  for (let i = 0; i < snake.length; i++) {
    ctx.fillStyle = i === 0 ? "#006400" : "#228B22";
    ctx.fillRect(snake[i].x, snake[i].y, box, box);
    ctx.strokeStyle = "white";
    ctx.strokeRect(snake[i].x, snake[i].y, box, box);
  }

  // Draw food
  ctx.fillStyle = "red";
  ctx.fillRect(food.x, food.y, box, box);

  // Old head position
  let snakeX = snake[0].x;
  let snakeY = snake[0].y;

  // Move direction
  if (d === "LEFT") snakeX -= box;
  if (d === "UP") snakeY -= box;
  if (d === "RIGHT") snakeX += box;
  if (d === "DOWN") snakeY += box;

  // If snake eats the food
  if (snakeX === food.x && snakeY === food.y) {
    score++;
    placeFood();
  } else {
    // Remove tail
    snake.pop();
  }

  // Add new head
  const newHead = { x: snakeX, y: snakeY };

  // Game over conditions
  if (
    snakeX < 0 ||
    snakeX >= canvas.width ||
    snakeY < 0 ||
    snakeY >= canvas.height ||
    collision(newHead, snake)
  ) {
    clearInterval(game);
    saveScore(playerName, score);
    displayGameOver(score);
  }

  snake.unshift(newHead);

  // Draw Score
  ctx.fillStyle = "#006400";
  ctx.font = "20px Changa one";
  ctx.fillText("Score: " + score, box, 0.8 * box);
}

function drawInitialScreen() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#aaa";
  ctx.font = "30px Changa one";
  ctx.fillText("Press Key to Start", canvas.width / 2.5, canvas.height / 2);
}

function collision(head, array) {
  for (let i = 0; i < array.length; i++) {
    if (head.x === array[i].x && head.y === array[i].y) return true;
  }
  return false;
}

function saveScore(name, score) {
  let scores = JSON.parse(localStorage.getItem("scoreHistory") || "[]");
  const date = new Date().toLocaleDateString();
  scores.push({ name, score, date });
  localStorage.setItem("scoreHistory", JSON.stringify(scores));
}

function displayGameOver(finalScore) {
  document.getElementById("finalScore").innerText = finalScore;
  document.getElementById("gameOverModal").style.display = "flex";
}

function startGameAgain() {
  document.getElementById("gameOverModal").style.display = "none";
  initializeGame();
}

initializeGame();
