function calculate() {
    const sel = $('.action-select:checked').length;
    const cnt = $('.action-select').length;
    var str = 'Выбрано ' + sel + ' записей из ' + cnt;
    $('span.action-counter').html(str);
}

function check_all() {
    var items = document.getElementsByName('_selected_action');
    for (var i = 0; items[i]; ++i) {
        if (items[i].checked == false) {
            items[i].checked = true;
        }
    }
    $("tbody>tr").addClass("selected");
}

function uncheck_all() {
    var items = document.getElementsByName('_selected_action');
    for (var i = 0; items[i]; ++i) {
        if (items[i].checked == true) {
            items[i].checked = false;
        }
    }
    $("tbody>tr").removeClass("selected");
}

document.getElementById('action-toggle').addEventListener('change', (event) => {
    event.target.checked ? check_all() : uncheck_all();
    calculate();
});

$(".action-select:checkbox").change(function () {
    calculate();
    $(this).parent().parent().toggleClass("selected")
});


function question(el, action) {
    td = el.parentElement
    tr = el.parentElement.parentElement;
    cells = tr.getElementsByTagName('td');
    created = cells[2].innerText;
    name = cells[3].innerText;
    quest = '';
    if (action == 'publish') quest = "ОПУБЛИКОВАТЬ статью ?";
    else if (action == 'unpublish') quest = "Вы уверены ?\nСнять с публикации данную статью ?";
    else if (action == 'delete') quest = "Вы уверены ?\nХоите УДАЛИТЬ данную статью ?";
    else {
        alert('Ошибка ввода!');
        return;
    }
    if (confirm(quest + "\n\nВремя создания:\n " + created + "\n\n" + name)) {
        uncheck_all();
        checkbox = tr.getElementsByClassName("action-select")[0];
        checkbox.checked = true;
        calculate();
        document.getElementById('action').value = action;
        document.getElementById('changelist-form').submit();
    }
}

function action_submit() {
    if ($('#action').val() == "none") {
        alert("Выберите необходимое действие !");
        return;
    }
    if ($('.action-select:checked').length == 0) {
        alert("Выберите статьи !");
        return;
    }
    document.getElementById('changelist-form').submit();
}

$(document).ready(function () {
    $('td.status').on('click', 'a', function (e) {
        e.preventDefault();
        tr = this.parentElement.parentElement;
        cells = tr.getElementsByTagName('td');
        created = cells[2].innerText;
        name = cells[3].innerText;
        url = this.href;
        arr = url.split('/');
        id = arr[arr.length - 2];
        status = arr[arr.length - 1];
        if (status != 0) quest = "ОПУБЛИКОВАТЬ статью ?";
        else quest = "Вы уверены ?\nСнять с публикации данную статью ?";
        if (confirm(quest + "\n\nВремя создания:\n " + created + "\n\n" + name + "\n\n")) {
            $.ajax({
                url: url,
                type: 'GET',
                success: function (res) {
                    $('#status_' + id).empty();
                    $('#status_' + id).hide().fadeIn(500).html(res);
                },
                error: function () {
                    alert('Error');
                }
            });
            $(this.parentElement).toggleClass('draft')
        }
    });
});