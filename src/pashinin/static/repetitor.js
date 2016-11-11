$(document).ready(function() {
	$("form#enrollform").submit(function(e){
		e.preventDefault();
		$.ajax({
			type: 'POST',
			url: $(this).attr('action'),
			data: $.extend({
				'cmd': 'enroll'
			}, $(this).serializeObject()),
			context: this,
			dataType: 'json',
			success: function(d){
				if ("errors" in d){
					var errors = d["errors"];
					showFormErrors(errors, $("form#enrollform"));
				}else{
					alert("Спасибо, я перезвоню Вам как только освобожусь.");
				}
			}
		});
		return false;
	});

});
