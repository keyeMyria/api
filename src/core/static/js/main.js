function closest(el, selector) {
	const matchesSelector = el.matches || el.webkitMatchesSelector || el.mozMatchesSelector || el.msMatchesSelector;
	while (el) {
		if (matchesSelector.call(el, selector)) {
			return el;
		} else {
			el = el.parentElement;
		}
	}
	return null;
}
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
// getURLParameter('a') == 1;
function getURLParameter(name) {
	return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
}


// 3 following blocks are taken from django's docs to fix csrf errors
// https://docs.djangoproject.com/en/dev/ref/csrf/
// https://learn.javascript.ru/cookie#%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D1%8F-getcookie-name
function getCookie(name) {
	var matches = document.cookie.match(new RegExp(
		"(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
	));
	return matches ? decodeURIComponent(matches[1]) : undefined;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//         }
//     }
// });


function showFormErrors(errors, form) {
	// "errors" is a dictionary of form:
	// {formfield1: ["error1", "error2"], ...}
	Array.from(form.querySelectorAll('[class^=ERR]')).forEach(function(el) {
		el.parentNode.removeChild(el);
	});

	// fields errors
	for (var field in errors) {
		let msgs = errors[field];
		let msg0 = msgs[0];
		let input = form.querySelector("[name="+field+"]");
		let cls = 'ERR'+field;
		let msg = form.querySelector("div."+cls);
		if (!msg){
			msg = document.createElement('div');
			msg.className = cls;
			msg.style.color = '#f96430';
			msg.style.textAlign = 'left';
			msg.style.fontSize = '0.7rem';
		}
		msg.innerHTML='';
		msg.appendChild(document.createTextNode(msg0));
		if (input) input.parentNode.insertBefore(msg, input);
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

{let ready=function(e){
	let profile = document.getElementById("profile");
	if (profile) profile.addEventListener("click", function(e) {
		document.getElementById("profile").classList.toggle("pressed");
		document.getElementById("loginbox").classList.toggle("hide");
		e.stopPropagation();
		e.preventDefault();
	});

	let site_switch = document.getElementById("site_switch");
	if (site_switch) site_switch.addEventListener("click", function(e) {
		document.getElementById("site_switch").classList.toggle("pressed");
		document.getElementById("site_switch_menu").classList.toggle("hide");
		e.stopPropagation();
		e.preventDefault();
	});

	// hide any menu when clicked somewhere but not in menu
	document.addEventListener("click", function(e) {
		if (!closest(e.target, ".popup")) {
			let profile = document.getElementById("profile");
			if (profile) profile.classList.remove("pressed");
			let site_switch = document.getElementById("site_switch");
			if (site_switch) profile.classList.remove("pressed");

			Array.from(document.getElementsByClassName("popup")).forEach(function(el) {
				el.classList.add("hide");
			});
		}
	});

	let exit = document.getElementById("exit");
	if (exit) exit.addEventListener("click", function(e){
		e.preventDefault();
		fetch(e.target.getAttribute("href"),
			  {
				  method: 'POST',
				  credentials: 'same-origin',
				  headers: {
				  	  "X-CSRFToken": getCookie('csrftoken')
				  },
				  body: ""
			  })
			// .then(r => r.json())
			.then(r => {
				location.reload();
			});
	});
};

 if (document.readyState === 'complete' || document.readyState !== 'loading') {
	 ready();
 } else {
	 document.addEventListener('DOMContentLoaded', ready);
 };
}
