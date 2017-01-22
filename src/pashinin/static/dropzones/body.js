{let ready = function(e) {
	let upload_div = document.getElementById("bodyupload");
	upload_div.addEventListener("mouseover", function(e) {
		document.getElementById("bodyupload").classList.add('hide');
	});
	upload_div.addEventListener("mouseout", function(e) {
		document.getElementById("bodyupload").classList.add('hide');
	});

	// Not only files can be drag&dropped but also links, images...
	// We need to detect only files
	function containsFiles(e) {
		var t = e.dataTransfer.types;
		if (t) {
			if (t.length>1 && t[0] == "text/x-moz-url"){return false;}
			for (var i=0; i<t.length; i++) {
				if (t[i] == "Files") {
					return true;
				}
			}
		}
		return false;
	}
	var counter=0;
	let hide = function(e){document.getElementById('bodyupload').classList.add("hide");};
	new Dropzone(document.body, {
		url: "/_/file/upload", // Set the url
		//previewsContainer: "#previews", // Define the container to display the previews
		clickable: false, // Define the element that should be used as click trigger to select files.
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		},
		drop: function(e) {
			counter=0;
			document.getElementById('bodyupload').classList.add("hide");
		},
		dragend: function(e) {
			document.getElementById('bodyupload').classList.add("hide");
		},
		dragstart: function(e) {
			document.getElementById('bodyupload').classList.add("hide");
		},
		dragenter: function(e) {
			// console.log(e.dataTransfer);
			// console.log(e);
			// console.log(e.dataTransfer.types);
			counter++;
			if (containsFiles(e))
				document.getElementById('bodyupload').classList.remove("hide");
		},
		dragover: function(e) {
			if (containsFiles(e))
				document.getElementById('bodyupload').classList.remove("hide");
		},
		dragleave: function(e) {
			counter--;
			if (counter === 0) {
				document.getElementById('bodyupload').classList.add("hide");
			}
		},
		uploadprogress: function(file, progress, bytesSent) {
			var node, _i, _len, _ref, _results;
			if (file.previewElement) {
				_ref = file.previewElement.querySelectorAll("[data-dz-uploadprogress]");
				_results = [];
				for (_i = 0, _len = _ref.length; _i < _len; _i++) {
					node = _ref[_i];
					if (node.nodeName === 'PROGRESS') {
						_results.push(node.value = progress);
					} else {
						_results.push(node.style.width = "" + progress + "%");
					}
				}
				return _results;
			}
			return null;
		},
		addedfile: function(file) {
			return null;
		}
	});
};
 if (document.readyState === 'complete' || document.readyState !== 'loading') {
	 ready();
 } else {
	 document.addEventListener('DOMContentLoaded', ready);
 };
}
