function save_checkbox() {
    var name = this.id // Получить id(имя) объекта
    var id = name.slice(7)
    var action = this.checked
    $.ajax({
        url: "/api" + "/" + "answer" + "/" + id + "/" + action + "/",
        type: 'POST',
        data: {
            'obj': name,
        },
        headers: {'X-CSRFToken': csrftoken},
        success: function (json) {
            console.log("Sucses!!!")
        }
    });
}

document.addEventListener("DOMContentLoaded", function () // После загрузки всех объектов на странице
    {

        var list = document.querySelectorAll('[type="checkbox"]'); // Найти список чекбоксов

        for (var i = 0; i < list.length; i++) // Цикл по списку

        {
            list[i].addEventListener('click', save_checkbox) // Назначить чекбоксу обработчик, передать в него его индекс
        }
    }
)
