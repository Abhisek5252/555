// coin.js
const coin = document.querySelector('.coin');
const flipButton = document.querySelector('#flip-button');

let isHeads = false;

flipButton.addEventListener('click', () => {
  coin.classList.add('spinning');

  setTimeout(() => {
    const random = Math.random();

    if (random < 0.5) {
      isHeads = true;
      coin.style.transform = 'rotateY(0deg)';
    } else {
      isHeads = false;
      coin.style.transform = 'rotateY(180deg)';
    }

    coin.classList.remove('spinning');

    // Update UI or handle result here
  }, 3000);
});
