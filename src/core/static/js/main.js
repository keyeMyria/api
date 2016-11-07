// String.format()     "{1} text ... {2}".format()
if (!String.prototype.format) {
	String.prototype.format = function() {
		var args = arguments;
		return this.replace(/{(\d+)}/g, function(match, number) {
			return typeof args[number] != 'undefined'
				? args[number]
				: match
			;
		});
	};
}
String.prototype.isEmpty = function() {
    return (this.length === 0 || !this.trim());
};

function url_params(){
	var res = {};
	var query = window.location.search.substring(1);
	var vars = query.split('&');
	for (var i = 0; i < vars.length; i++) {
		var pair = vars[i].split('=');
		res[decodeURIComponent(pair[0])] = pair[1];
	}
	return res;
}

function getCookie(name) {
	var c, cookie, cookieValue, cookies, _i, _len;
	cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		cookies = document.cookie.split(';');
		for (_i = 0, _len = cookies.length; _i < _len; _i++) {
			c = cookies[_i];
			cookie = c.trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
};

$.ajaxSetup({  // MUST be in document.ready()
	beforeSend: function(xhr, settings) {
		function sameOrigin(url) {
			// url could be relative or scheme relative or absolute
			var host = document.location.host; // host + port
			var protocol = document.location.protocol;
			var sr_origin = '//' + host;
			var origin = protocol + sr_origin;
			// Allow absolute or scheme relative URLs to same origin
			return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
				(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
				// or any other URL that isn't scheme relative or absolute i.e relative.
				!(/^(\/\/|http:|https:).*/.test(url));
		}
		// if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
		// 	return xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		// }
		function safeMethod(method) {
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		}
		return null;
	}
});

function showFormErrors(errors, form) {
	// errors - {formfield1: ["error1", "error2"], ...}
	form.find("[class^=ERR]").remove();
	for (var name in errors) {
		let msgs = errors[name];
		var msg0 = msgs[0];
		var input = form.find("[name="+name+"]");
		var cls = 'ERR'+name;
		var err_block = form.find("div.{0}".format(cls));
		if (!err_block.length){
			err_block = $( '<div class="{0}"></div>'.format(cls) ).css({"font-size":"0.7rem","color":"red","text-align":"left"});
		}
		err_block.empty();
		err_block.append(document.createTextNode(msg0));
		err_block.insertBefore(input);
	}
};
