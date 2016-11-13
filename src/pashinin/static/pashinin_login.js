$(document).ready(function() {
	$("form#login").submit(function(e){
		e.preventDefault();
		$.ajax({
			type: 'POST',
			url: $(this).attr('action'),
			data: $(this).serializeObject(),
			context: this,
			dataType: 'json',
			success: function(d){
				if ("errors" in d){
					showFormErrors(d["errors"], $("form#login"));
				}else{
					window.location.href = getURLParameter('return');
				}
			}
		});
		return false;
	});
});
