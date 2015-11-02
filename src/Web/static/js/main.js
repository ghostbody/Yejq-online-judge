$(function () { $("[data-toggle='tooltip']").tooltip(); });

$(document).ready( function () {
    $("#user_change").click( function() {
	password = $("input[name=new_password]").val();
	nickname = $("input[name=new_nickname]").val();
	email = $("input[name=new_email]").val();
	phone = $("input[name=new_phone]").val();

	if(password == "" && nickname == "" && email == "" && phone == "") {
	    alert("No data input");
	} else {

	$.post(
	    "\main", 
	       {
		   new_password : password,
		   new_nickname : nickname,
		   new_email : email,
		   new_phone : phone 
	       },
	       function(data,status) {
		   alert("information changed!");
	       });
	$('#myModal').modal('hide');
	location.reload();
	}
    });

});

