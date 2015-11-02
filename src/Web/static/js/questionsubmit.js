
$(document).ready( function () {

  $('#statusModal').on('hidden.bs.modal', function (e) {
    $("#result").text("Waiting...");
    $("#report").text("");
    $("#result").css("color", "blue");
  });

  $("#code_submit").click( function() {
    var code = editor.getValue();
    //code = $("textarea[name=code]").val();
  	var language = $("select[name=language]").val();
    var pid = $("#pid").text();
    if(code == "" ) {
        alert("No data input");
    } else {
	    $.post(
        "\questions", 
        {
            pid : pid,
            code : code,
            language : language
        },
        function(data,status) {
        	alert("submit success");
          $("#statusModal").modal("show");
          var runid = data.runid;
          function getResult() {
            $.get(
              "\questions?operation=getResult", 
              {
                  runid : runid
              },
              function(data, status) {
                if(data.remark != 0) {
                  $("#result").hide();
                  $("#result").text("Points:" + data.grade);
                  $("#report").text(data.report);
                  if(data.grade == "100") {
                    $("#result").css("color","green");
                  } else if (data.grade != "0") {
                    $("#result").css("color", "orange");
                  } else {
                    $("#result").css("color", "red");
                  }
                  $("#result").show(1200);
                  gResult = window.clearInterval(gResult);
                }
              }
            )
          }
          gResult = setInterval(getResult, 3000);
        }
      );
	   }
  });
});