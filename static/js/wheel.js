// wheel.js
const wheel = document.querySelector('.wheel');
const spinButton = document.querySelector('#spin-button');
const claimButton = document.querySelector('.claim-button');
const slices = document.querySelectorAll('.wheel-slice');

let spinCount = 0;
let currentSlice = 0;

const rewards = ['Reward 1', 'Reward 2', 'Reward 3', 'Reward 4'];

// Initialize wheel with rewards
rewards.forEach((reward, index) => {
  const slice = slices[index];
  slice.textContent = reward;
});

spinButton.addEventListener('click', () => {
  spinCount++;
  wheel.classList.add('spinning');

  // Calculate random spin duration
  const spinDuration = getRandomInteger(3, 5);

  setTimeout(() => {
    // Determine the winning slice
    currentSlice = getRandomInteger(0, slices.length - 1);
    // Set the active slice
    slices.forEach((slice, index) => {
      slice.classList.remove('active');
      if (index === currentSlice) {
        slice.classList.add('active');
      }
    });

    // Update the UI with the claim button
    claimButton.style.display = 'block';
    claimButton.textContent = `Claim ${rewards[currentSlice]}`;

    wheel.classList.remove('spinning');
  }, spinDuration * 1000);
});

claimButton.addEventListener('click', () => {
  // Handle reward claiming logic here
  console.log(`You won ${rewards[currentSlice]}!`);

  // Reset claim button
  claimButton.style.display = 'none';
});
