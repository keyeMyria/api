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

// ?a=1&b=2
// myvar = getURLParameter('a');
function getURLParameter(name) {
	return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
}


// 3 following blocks are taken from django's docs to fix csrf errors
// https://docs.djangoproject.com/en/dev/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});



function showFormErrors(errors, form) {
	// "errors" is a dictionary of form:
	// {formfield1: ["error1", "error2"], ...}
	form.find("[class^=ERR]").remove();
	// fields errors
	for (var field in errors) {
		let msgs = errors[field];
		var msg0 = msgs[0];
		var input = form.find("[name="+field+"]");
		var cls = 'ERR'+field;
		var err_block = form.find("div.{0}".format(cls));
		if (!err_block.length){
			err_block = $( '<div class="{0}"></div>'.format(cls) ).css({"font-size":"0.7rem","color":"#f96430","text-align":"left"});
		}
		err_block.empty();
		err_block.append(document.createTextNode(msg0));
		err_block.insertBefore(input);
	}

	// form errors
	// special field "__all__"
	let form_errors = errors['__all__'];
	if (form_errors){
		for (let err in form_errors) {
			alert(form_errors[err]);
		}
	}
};

$(document).ready(function() {
	$("a#profile").click(function(){
		$("#loginbox").toggleClass("hide");
		return false;
	});

	// hide popup menus when clicked elsewhere
	$(document).click(function(event) {
		if (!$(event.target).closest(".popup").length) {
			$(".popup").addClass("hide");
		}
	});
	$("#exit").click(function(){
		$.ajax({
			type: 'POST',
			url: $(this).attr('href'),
			data: {'logout':true},
			context: this,
			dataType: 'json',
			success: function(d){
				location.reload();
			}
		});
		return false;
	});
});
