function nextpage() {
    const url = new URL(window.location);
    let page_num = parseInt(url.searchParams.get('page')) + 1;
    if (isNaN(page_num)) {
        page_num = 1;
    }
    window.location.href = '?page=' + page_num;
}

function previouspage() {
    const url = new URL(window.location);
    let page_num = parseInt(url.searchParams.get('page')) - 1;
    if (page_num < 1 || isNaN(page_num)) {
        page_num = 1;
    }
    window.location.href = '?page=' + page_num;
}



// Добавьте активный класс к текущей кнопке (выделите его)
var header = document.getElementById("pages");
var btns = header.getElementsByClassName("btn1");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
  var current = document.getElementsByClassName("active");
  current[0].className = current[0].className.replace(" active", "");
  this.className += " active";
  });
}
