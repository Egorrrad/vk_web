// Выбираем все элементы с классом like
const likes = document.querySelectorAll('.like');

// В каждом элементе выбираем плюс и минус. Навешиваем на событие клик функцию render()

likes.forEach(like => {

  //получаем id вопроса
  const id = like.id.split('_')[1];
  const plus = like.querySelector('.like-button');

  const minus = like.querySelector('.dislike-button');

  const counter_element = like.querySelector('.like-count');

  let counter = 0;

  plus.addEventListener('click', () => {
    render(++counter, counter_element);


  });

  minus.addEventListener('click', () => {
    render(--counter, counter_element)
  });

});

// Функция обновляет текст
const render = (counter, counter_element) => counter_element.innerText = counter;