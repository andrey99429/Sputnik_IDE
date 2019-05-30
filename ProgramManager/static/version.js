var buttons = ['#save_as_new', '#save', '#build', '#build_and_run'];
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
        console.log(msg);
        //$("#console").html(msg);
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
        console.log('save_as_new');
        load(true, false, false);
    });

    $(document).on('click', '#save', function () {
        console.log('save');
        load(false, false, false);
    });

    $(document).on('click', '#build', function () {
        console.log('build');
        load(false, true, false);
    });

    $(document).on('click', '#build_and_run', function () {
        console.log('build_and_run');
        load(false, true, true);
    });
});