/* global fetch, serialize, formToJSON, getCookie, showFormErrors, getURLParameter */
{
  const ready = () => {
    document.getElementById('login').addEventListener('submit', (e) => {
      e.preventDefault();
      const form = e.target;
      fetch(e.target.getAttribute('action'), {
        method: 'POST',
        credentials: 'include',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          Accept: 'application/json',
          'Content-type': 'application/x-www-form-urlencoded',
        },
        body: serialize(formToJSON(form.elements)),
      })
        .then(r => r.json())
        .then((data) => {
          if ('errors' in data) {
            showFormErrors(data.errors, document.getElementById('login'));
          } else {
            window.location.href = getURLParameter('return');
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
