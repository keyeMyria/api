{let ready=function(e) {
	// "Show log" links in "Updates" page
	let links = document.querySelectorAll("a.log");
	for (let i = 0; i < links.length; i++) {
		let el = links[i];
		el.addEventListener("click", function(e) {
			e.target.parentElement.querySelector("div.log").classList.toggle("hide");
			e.preventDefault();
			let a=toInt("a");
		});
	};
};
 if (document.readyState === 'complete' || document.readyState !== 'loading') {
	 ready();
 } else {
	 document.addEventListener('DOMContentLoaded', ready);
 }
}
