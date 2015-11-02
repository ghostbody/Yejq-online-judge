
$(document).ready(function () {

    $("#post").click(function() {
        var content = $("#comment").val();
        $.post(
            "discuss",
            {
                method : "comment",
                content : content
            },
            function(data,status) {
                alert(data);
                 window.location.reload();
            }
        )
    });

    $("body").on("click", ".reply", function(event) {
        var target = $(event.target);
        repid = target.data("uid");
    });

    $("#reply").click(function() {
        var content = $("#recontent").val();
        $.post(
            "discuss",
            {
                method : "reply",
                content : content,
                repuid : repid
            },
            function(data,status) {
                alert(data);
                 window.location.reload();
            }
        )
    });

})