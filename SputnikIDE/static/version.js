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
    var date = new Date();
    var time_str = '[' + date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds() + '] ';
    var success_text = time_str;
    var danger_text = time_str;
    $('#console').html(' ');

    if (response['saved']) {
        success_text += '<br></be><strong>Версия сохранена.</strong>';
    } else {
        danger_text += '<br><strong>Ошибка!</strong> Версия не сохранена.';
    }

    $('#console').append(response['build_out']);
    if (response['build_err']) {
        danger_text += '<br><strong>Ошибка!</strong> Build error.';
        $('#console').append(response['build_err']);
    } else {
        success_text += '<br><strong>Build successful.</strong>';
        $('#console').append(response['run_out']);
        $('#console').append(response['run_err']);
    }
    if (success_text !== time_str) {
        $('.response-status').append(create_alert('success', success_text));
    }
    if (danger_text !== time_str) {
        $('.response-status').append(create_alert('danger', danger_text));
    }
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