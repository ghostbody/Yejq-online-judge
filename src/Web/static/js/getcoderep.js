$(document).ready( function () {
    $("body").on("click", ".source", function(event) {
        target = $(event.target);
        runid = target.data("runid");
        uid = target.data("uid");
        language = target.data("language");
            $.get(
            "\s-getcode", 
            {
                language : language,
                runid : runid,
                uid : uid
            },
            function(data,status) {
                $("#codecontent").text(data)
                $("#myModal").modal().show();
            });
    });

    $("body").on("click", ".report", function(event) {
        target = $(event.target);
        runid = target.data("runid");
            $.get(
            "\s-getreport", 
            {
                runid : runid
            },
            function(data,status) {
                $("#codecontent1").text(data)
                $("#myModal1").modal().show();
            });
    });
});