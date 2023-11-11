// Выбираем все элементы с классом like

/*

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
      $.ajax({
        url : "question" +"/" + id + "/" + like + "/",
        type : 'POST',
        data : { 'obj' : id },

        success : function (json) {
            //like.find("[data-count='like']").text(json.like_count);
            //dislike.find("[data-count='dislike']").text(json.dislike_count);
            counter = json.sum_rating
        }
    });
    render(counter, counter_element);


  });

  minus.addEventListener('click', () => {
      dislike()
    render(--counter, counter_element)
  });

});

// Функция обновляет текст
const render = (counter, counter_element) => counter_element.innerText = counter;


 */


const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

const csrftoken = getCookie("csrftoken");


function like() {
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();
    //var alllikes = dislike.next()


    const alllikes = document.getElementById('like_' + pk)
    const counter_element = alllikes.querySelector('.like-count');

    /*
        var btn = document.getElementById('likebut_'+pk);
        var list = btn.classList;
        console.log(list)
        btn.classList.add("active");



     */
    var url = "api" + "/" + "question" + "/" + pk + "/" + action + "/";

    $.ajax({
        url: "/api" + "/" + type + "/" + pk + "/" + action + "/",
        type: 'POST',
        data: {
            'obj': pk,
        },
        headers: {'X-CSRFToken': csrftoken},
        //CsrfViewMiddleware: csrftoken,
        success: function (json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            //alllikes.find("[data-count='alllike']").text(json.sum_rating)
            counter_element.innerText = json.sum_rating
            //console.log(counter_element.innerText)
            //console.log(alllikes.find("[data-count='alllike']"))
        }
    });

    return false;
}

function dislike() {
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();
    //var alllikes = dislike.next()
    const alllikes = document.getElementById('like_' + pk)
    const counter_element = alllikes.querySelector('.like-count');

    var url = "api" + "/" + "question" + "/" + pk + "/" + action + "/";
    $.ajax({
        url: "/api" + "/" + type + "/" + pk + "/" + action + "/",
        type: 'POST',
        data: {'obj': pk},
        headers: {'X-CSRFToken': csrftoken},
        success: function (json) {
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like.find("[data-count='like']").text(json.like_count);
            counter_element.innerText = json.sum_rating
            //alllikes.find("[data-count='alllike']").text(json.sum_rating)
            //console.log(alllikes.innerText)
            //console.log(alllikes.find("[data-count='alllike']"))
        }
    });

    return false;
}

// Подключение обработчиков
$(function () {
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
});