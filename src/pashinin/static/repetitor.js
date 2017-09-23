/* global fetch, serialize, formToJSON, getCookie, showFormErrors, alert */
{
  const ready = () => {
    // main page, enroll button
    document.getElementById('enrollform').addEventListener('submit', (e) => {
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
            showFormErrors(data.errors, document.getElementById('enrollform'));
          } else {
            alert('Спасибо, я перезвоню Вам как только освобожусь.');
          }
        });
    });

    // City switcher
    // document.getElementById('city_switcher').addEventListener('click', (e) => {
    //   e.preventDefault();
    //   const el = document.getElementById('overlay');
    //   if (el.style.visibility === 'visible') {
    //     el.style.visibility = 'hidden';
    //     // document.getElementById('body').style.filter = '';
    //   } else {
    //     el.style.visibility = 'visible';
    //     // document.getElementById('body').style.filter = 'blur(5px)';
    //   }
    //   // el.style.visibility = (el.style.visibility === 'visible') ? 'hidden' : 'visible';
    //   // document.getElementById('body').style.filter = 'blur(5px)';
    //   // filter: blur(5px);
    // });

    // modal window close on click
    // document.getElementById('overlay').addEventListener('click', (e) => {
    //   e.preventDefault();
    //   const el = document.getElementById('overlay');
    //   el.style.visibility = 'hidden';
    // });
    // document.getElementById('overlay-content').addEventListener('click', (e) => {
    //   e.stopPropagation();
    // });
  };
  if (document.readyState === 'complete' || document.readyState !== 'loading') {
    ready();
  } else {
    document.addEventListener('DOMContentLoaded', ready);
  }
}
