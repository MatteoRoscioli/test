<!DOCTYPE html>
<html>
<head>
  <title>Airplane Simulator</title>
  <style>
    canvas {
      border: 1px solid black;
    }
  </style>
</head>
<body>
  <canvas id="myCanvas" width="800" height="600"></canvas>
  <script>
    // Get the canvas element
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");

    // Initialize the airplane's position and velocity
    var x = 400;
    var y = 300;
    var vx = 0;
    var vy = 0;
    var speed = 5;

    // Define the airplane's dimensions
    var planeWidth = 50;
    var planeHeight = 30;

    // Function to draw the airplane
    function drawAirplane() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.beginPath();
      ctx.rect(x - planeWidth / 2, y - planeHeight / 2, planeWidth, planeHeight);
      ctx.fillStyle = "blue";
      ctx.fill();
      ctx.closePath();
    }

    // Function to update the airplane's position
    function updateAirplane() {
      // Update the airplane's position based on the velocity
      x += vx;
      y += vy;

      // Check for screen boundaries and adjust the velocity accordingly
      if (x - planeWidth / 2 < 0 || x + planeWidth / 2 > canvas.width) {
        vx = -vx;
      }
      if (y - planeHeight / 2 < 0 || y + planeHeight / 2 > canvas.height) {
        vy = -vy;
      }
    }

    // Game loop
    function gameLoop() {
      // Update the airplane's position
      updateAirplane();

      // Draw the airplane
      drawAirplane();

      // Request the next frame
      requestAnimationFrame(gameLoop);
    }

    // Start the game loop
    gameLoop();
  </script>
</body>
</html>