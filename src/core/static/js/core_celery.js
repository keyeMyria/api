$(document).ready(function() {
	$("a#run_celery").click(function(){
		$.ajax({
			type: 'POST',
			url: $(this).attr('href'),
			data: {'start':true},
			context: this,
			dataType: 'json',
			success: function(d){
				// location.reload();
				console.log(d);
			}
		});
		return false;
	});
});
