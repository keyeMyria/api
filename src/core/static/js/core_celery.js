$(document).ready(function() {
	// var url = $("form.api").attr("action");
	var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	var ws_path = ws_scheme + '://' + window.location.host + "/admin/celery";
	var ws = new WebSocket(ws_path);
	ws.onopen = function() {
		console.log("websocket connected");
	};
	ws.onmessage = function(e) {
		console.log("Received: " + e.data);
	};
	ws.onerror = function(e) {
		console.error(e);
	};
	ws.onclose = function(e) {
		console.log("connection closed");
	};

	$("a#run_celery").click(function(){
		ws.send('{"key": "value"}');
		// $.ajax({
		// 	type: 'POST',
		// 	url: $(this).attr('href'),
		// 	data: {'start':true},
		// 	context: this,
		// 	dataType: 'json',
		// 	success: function(d){
		// 		// location.reload();
		// 		console.log(d);
		// 	}
		// });
		return false;
	});
});
