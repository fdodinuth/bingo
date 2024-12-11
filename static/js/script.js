function pickRandomNumber() {
  fetch('/pick_random', {
      method: 'POST'
  })
  .then(response => response.json())
  .then(data => {
      // Show the called number with animation
      const numberElement = document.getElementById('random-number');
      numberElement.innerText = `Number Called: ${data.number}`;
      numberElement.classList.add('animate');

      // Remove animation class after 5 seconds
      setTimeout(() => {
          numberElement.classList.remove('animate');
          // Add green color to the latest number after the animation
          numberElement.classList.add('green');
      }, 5000); // 5 seconds duration

      // Update the called numbers container in the Host Page
      let calledNumbersContainer = document.getElementById('called-numbers-container');
      let numberBox = document.createElement('div');
      numberBox.classList.add('number-box');
      numberBox.innerText = data.number;
      calledNumbersContainer.appendChild(numberBox);

      // Highlight the called number box in gray
      numberBox.classList.add('called');

      // Show which players have this number
      let playersWithNumberList = document.getElementById('players-with-number');
      playersWithNumberList.innerHTML = ''; // Clear previous list
      data.players.forEach(player => {
          let playerItem = document.createElement('li');
          playerItem.textContent = `${player} has ${data.number}`;
          playersWithNumberList.appendChild(playerItem);
      });

      // Play a random sound if there are players with the called number
      if (data.players.length > 0) {
          playRandomSound();
      }
  });
}

function playRandomSound() {
  // Array of sound files (ensure you replace with your actual sound file paths)
  const sounds = [
      "/static/sounds/sound1.mp3",
      "/static/sounds/sound2.mp3",
      "/static/sounds/sound3.mp3",
      "/static/sounds/sound4.mp3",
      "/static/sounds/sound5.mp3",
      "/static/sounds/sound6.mp3",
      "/static/sounds/sound7.mp3",
      "/static/sounds/sound8.mp3",
      "/static/sounds/sound9.mp3",
      "/static/sounds/sound10.mp3"
  ];

  // Select a random sound
  const randomSound = sounds[Math.floor(Math.random() * sounds.length)];

  // Create an audio element to play the sound
  const audio = new Audio(randomSound);

  // Play the sound
  audio.play();

  // Stop the sound after 5 seconds
  setTimeout(() => {
      audio.pause();
      audio.currentTime = 0; // Reset sound to the start
  }, 5000); // Stop sound after 5 seconds
}
