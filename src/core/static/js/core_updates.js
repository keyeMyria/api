$(document).ready(function() {
	$("a.log").click(function(){
		$(this).parent().find("div.log").toggleClass("hide");
		return false;
	});
});
