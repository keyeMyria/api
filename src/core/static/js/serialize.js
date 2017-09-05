/**
 * Convert a dictionary to an URL query
 *
 * Example:
 * > serialize({1:2})
 * > "1=2"
 *
 * @param {dict} obj
 * @param {string} prefix
 * @return {string}
 */
// TODO: keys order?
window.serialize = (obj, prefix) => {
  const str = [];
  Object.keys(obj).forEach((parameter) => {
    const k = prefix ? `${prefix}[${parameter}]` : parameter;
    const v = obj[parameter];
    if (v !== null && typeof v === 'object') {
      str.push(window.serialize(v, k));
    } else {
      str.push(`${encodeURIComponent(k)}=${encodeURIComponent(v)}`);
    }
    // str.push((v !== null && typeof v === 'object') ?
    //          serialize(v, k) : `${encodeURIComponent(k)}=${encodeURIComponent(v)}`);
    // }
  });
  return str.join('&');
};
window.toJSON = (form) => {
  const obj = {};
  const inputs = form.querySelectorAll('input, select, textarea');
  // for (let i = 0; i < elements.length; i += 1) {
  inputs.forEach((input) => {
    // const element = elements[i];
    // const name = input.name;
    // const value = input.value;

    if (input.name) {
      obj[input.name] = input.value;
    }
  // }
  });
  return obj;
};

const isValidElement = el => el !== undefined && el.name && el.value && el.type !== 'submit';

window.formToJSON = elements => [].reduce.call(elements, (data, el) => {
  // if (el.type != "submit")
  const d = data;
  if (isValidElement(el)) {
    d[el.name] = el.value;
  }
  return d;
}, {});
