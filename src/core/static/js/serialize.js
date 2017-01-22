function serialize(obj, prefix) {
	var str = [], p;
	for(p in obj) {
		if (obj.hasOwnProperty(p)) {
			var k = prefix ? prefix + "[" + p + "]" : p, v = obj[p];
			str.push((v !== null && typeof v === "object") ?
					 serialize(v, k) :
					 encodeURIComponent(k) + "=" + encodeURIComponent(v));
		}
	}
	return str.join("&");
};
function toJSON( form ) {
	var obj = {};
	var elements = form.querySelectorAll( "input, select, textarea" );
	for( var i = 0; i < elements.length; ++i ) {
		var element = elements[i];
		var name = element.name;
		var value = element.value;

		if( name ) {
			obj[ name ] = value;
		}
	}

	return obj;
	// return JSON.stringify( obj );
};

const isValidElement = el => {
	return el.name && el.value && el.type!="submit";
};
const formToJSON = elements => [].reduce.call(elements, (data, el) => {
	// if (el.type != "submit")
	if (isValidElement(el)) {
		data[el.name] = el.value;
	}
	return data;
}, {});
