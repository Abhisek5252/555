// hamster.js
const hamster = document.querySelector('.hamster');

hamster.addEventListener('click', () => {
  hamster.classList.add('flashing');

  setTimeout(() => {
    hamster.classList.remove('flashing');
  }, 1000);
});
