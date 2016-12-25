$(document).ready(function() {
	// var url = $("form.api").attr("action");
	var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	var ws_path = ws_scheme + '://' + window.location.host + "/admin/celery";
	var ws = new WebSocket(ws_path);
	ws.onopen = function() {
		console.log("websocket connected");
		$("#log").val("");
	};
	ws.onmessage = function(e) {
		let data = JSON.parse(e.data),
			stream = data['s'],  // stream
			d = data['p'];    // payload
		// console.log(e.data);
		try {
			$("#log").val($("#log").val()+d["logline"]);
		} catch (err) {

			// обработка ошибки

		}
	};
	ws.onerror = function(e) {
		console.error(e);
	};
	ws.onclose = function(e) {
		console.log("connection closed");
	};

	$("a#run_celery").click(function(){
		ws.send(JSON.stringify({"p": {"key": "value"}, "s": ""}));
		// ws.send(JSON.stringify({"payload": {"key": "value"}, "stream": "0"}));
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
