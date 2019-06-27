var buttons = ['#save_as_new', '#save', '#build', '#build_and_run'];

function create_alert(type, text) {
    return '<div class="alert alert-'+type+' alert-dismissible fade show" role="alert">' +
        text +
        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
        '<span aria-hidden="true">&times;</span>' +
        '</button>' +
        '</div>';
}

function parse_response(response) {
    /*
    saved
    build_out
    build_err

    run_out
    run_err
     */
    // $("#console").html(msg['run_out']);
    var date = new Date();
    var time_str = "[" + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds() + "] ";
    $('#console').html(' ');

    if (response['saved']) {
        $('.response-status').append(create_alert('success', time_str+'<strong>Версия сохранена!</strong>'));
    } else {
        $('.response-status').append(create_alert('danger', time_str+'<strong>Ошибка!</strong> Версия не сохранена.'));
    }

    if (response['build_err']) {
        $('#console').append(response['build_err']);
    } else {
        $('#console').append(response['run_out']);
        $('#console').append(response['run_err']);
    }

    console.log(response);
}

function load(new_version, build, run) {
    for (var button in buttons) {
        $(buttons[button]).prop('disabled', true);
    }
    var data = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'code': editor.getValue(),
        'new_version': new_version,
        'build': build,
        'run': run
    };

    var request = $.ajax({
        url: version_loading_url,
        method: 'POST',
        data: data,
    });
    request.done(function(msg) {
        for (var button in buttons) {
            $(buttons[button]).prop('disabled', false);
        }

        parse_response(msg);
    });
    request.fail(function(jqXHR, textStatus) {
        for (var button in buttons) {
            $(buttons[button]).prop('disabled', false);
        }
        //$("#console").html(textStatus);
    });
}

$(document).ready(function () {
    $(document).on('click', '#save_as_new', function () {
        load(true, false, false);
    });

    $(document).on('click', '#save', function () {
        load(false, false, false);
    });

    $(document).on('click', '#build', function () {
        load(false, true, false);
    });

    $(document).on('click', '#build_and_run', function () {
        load(false, true, true);
    });
});