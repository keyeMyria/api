{let ready=function() {
	document.getElementById("enroll").addEventListener("submit", function(e) {
		e.preventDefault();
		let form = e.target;
		fetch(form.getAttribute("action"), {
			method: 'POST',
			credentials: 'include',
			headers: {
				"X-CSRFToken": getCookie('csrftoken'),
				"Accept": "application/json",
				"Content-type": "application/x-www-form-urlencoded"
			},
			body: serialize(formToJSON(form.elements))
		})
			.then(r => r.json())
			.then(data => {
				if ("errors" in data){
					showFormErrors(data["errors"], document.getElementById("enroll"));
				}else{
					alert("Спасибо, я перезвоню Вам как только освобожусь.");
				}
			});
	});

    document.getElementById("cancel_enroll").addEventListener("click", function(e) {
        e.preventDefault();
        let form = e.target.closest("form");
        fetch(form.getAttribute("action"), {
            method: 'POST',
            credentials: 'include',
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                "Accept": "application/json",
                "Content-type": "application/x-www-form-urlencoded"
            },
            body: serialize({ 'action': 'cancel' })
        })
            .then(r => r.json())
            .then(data => {
                if ("errors" in data) {
                    showFormErrors(data["errors"], document.getElementById("enroll"));
                } else {
                    form.reset();
                    document.querySelector('.enroll-status-indb').classList.add('hide');
                    document.querySelector('.enroll-status-no').classList.remove('hide');
                }
            });
    });
};
 if (document.readyState === 'complete' || document.readyState !== 'loading') {
     ready();
 } else {
     document.addEventListener('DOMContentLoaded', ready);
 }
}
