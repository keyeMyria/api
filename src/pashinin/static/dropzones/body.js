$(document).ready(function() {
	$("#bodyupload").mouseenter(function() {
		$("#bodyupload").addClass('hide');
	});
	$("#bodyupload").mouseleave(function() {
		$("#bodyupload").addClass('hide');
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
	var show = function(e){
		if (containsFiles(e))
			document.getElementById('bodyupload').classList.remove("hide");
	};
	var hide = function(e){document.getElementById('bodyupload').classList.add("hide");};
	new Dropzone(document.body, {
		url: "/_/file/upload", // Set the url
		//previewsContainer: "#previews", // Define the container to display the previews
		clickable: false, // Define the element that should be used as click trigger to select files.
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		},
		drop: function(e) {
			return hide(e);
		},
		dragend: function(e) {
			return hide(e);
		},
		dragstart: function(e) {
			// console.log(e);
			return hide(e);
		},
		dragenter: function(e) {
			// console.log(e.dataTransfer);
			// console.log(e);
			// console.log(e.dataTransfer.types);
			return show(e);
		},
		dragover: function(e) {
			return show(e);
		},
		dragleave: function(e) {
			return hide(e);
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
});
