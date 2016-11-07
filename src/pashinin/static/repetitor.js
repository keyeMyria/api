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
				// var t = document.querySelector('#egerow'),
				// 	a = t.content.querySelector("a");
				// a.textContent = "1235646565";
				// var clone = document.importNode(t.content, true);
				// document.querySelector('#egelist').appendChild(clone);
			}
		});
		return false;
	});

	// $("#enroll").click(function(){
	// 	var f = $(this).closest("form");
	// 	var url = f.attr("action");
	// 	$.post(url, {
    //         'name': 'writerev',
	// 		'phone': 'writerev',
	// 		'message': 'writerev'
    //     }, function(data) {
	// 		console.log(data);
    //         // if (!handleError(data)) {
	// 		// 	return $("#backToArticleView").click();
    //         // }
    //     }, "json");
	// 	return false;
	// });
});
