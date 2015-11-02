
$(document).ready(function () {
    $('#reset').on('click', function() {
        $("#input").val("");
        $("#output").val("");
    });

    $('#submit').on('click', function() {
        var $btn = $(this).button('loading')
        var code = editor.getValue();
        var input = $('#input').val();
        var language = $("select[name=language]").val();
        if(code == "") {
            alert("No Code Input!");
            $btn.button('reset');
            return false;
        } else if(input == "") {
            alert("Warning: No input data to the Program!");
        }

        $.post(
                "/compiler",
                {
                    code: code,
                    input: input,
                    language: language
                },
                function(data, status) {
                    $("#output").val(data);
                }
            );
        $btn.button('reset');
    });
});