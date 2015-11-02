
var rejudgeFlag = true;

$(document).ready( function () {
    $("body").on("click", ".rejudge", function(event) {
        if(!rejudgeFlag) {
          alert("waiting for another task!");
          return false;
        }
        rejudgeFlag = false;
        target = $(event.target);
        runid = target.data("runid");
        target.removeClass("rejudge");
        target.removeClass("btn-info");
        target.addClass("kill");
        target.addClass("btn-danger");
        $(target).text("Kill");
        $.get("/s-admin?operation=rejudge",
            {
                runid : runid
            },
            function(data) {
                $(target).parent().prev().prev().prev().text("waiting");
                  function getResult(mytarget, myrunid) {
                    $.get(
                      "\questions?operation=getResult", 
                      {
                          runid : myrunid
                      },
                      function(data, status) {
                        if(data.remark != 0) {
                          $(mytarget).parent().prev().prev().prev().text(data.grade);
                          mytarget.addClass("rejudge");
                          mytarget.addClass("btn-info");
                          mytarget.removeClass("kill");
                          mytarget.removeClass("btn-danger");
                          $(mytarget).text("Rejudge");
                          gResult = window.clearInterval(gResult);
                          rejudgeFlag = true;
                        }
                      }
                    )
                  }
                var gResult = setInterval(getResult, 3000, target, runid);
            }
        );
    });

    $("body").on("click", ".kill", function(event) {
        target = $(event.target);
        runid = target.data("runid");
        $.get("/s-admin?operation=kill",
            {
                runid : runid
            },
            function(data) {
              target.addClass("rejudge");
              target.addClass("btn-info");
              target.removeClass("kill");
              target.removeClass("btn-danger");
              $(target).text("Rejudge");
              $(target).parent().prev().prev().prev().text("0");
            }
        )
    });

    $("body").on("click", ".validate", function(event) {
        target = $(event.target);
        pid = target.data("pid");
        $.get("/s-admin?operation=validate",
            {
              pid : pid
            },
            function(data) {
              target.addClass("btn-danger");
              target.removeClass("btn-success");
              target.addClass("invalidate");
              target.removeClass("validate");
              $(target).text("Invalidate");
            }
        )
    });

    $("body").on("click", ".invalidate", function(event) {
        target = $(event.target);
        pid = target.data("pid");
        $.get("/s-admin?operation=invalidate",
            {
              pid : pid
            },
            function(data) {
              target.addClass("btn-success");
              target.removeClass("btn-danger");
              target.addClass("validate");
              target.removeClass("invalidate");
              $(target).text("Validate");
            }
        )
    });

    $("body").on("click", ".uservalidate", function(event) {
        target = $(event.target);
        uid = target.data("uid");
        $.get("/s-admin?operation=uservalidate",
            {
              uid : uid
            },
            function(data) {
              target.addClass("btn-danger");
              target.removeClass("btn-success");
              target.addClass("userinvalidate");
              target.removeClass("uservalidate");
              $(target).text("Invalidate");
              $(target).parent().prev().prev().prev().prev().text("1");
            }
        )
    });

    $("body").on("click", ".userinvalidate", function(event) {
        target = $(event.target);
        uid = target.data("uid");
        $.get("/s-admin?operation=userinvalidate",
            {
              uid : uid
            },
            function(data) {
              target.addClass("btn-success");
              target.removeClass("btn-danger");
              target.addClass("uservalidate");
              target.removeClass("userinvalidate");
              $(target).text("Validate");
              $(target).parent().prev().prev().prev().prev().text("0");
            }
        )
    });

});