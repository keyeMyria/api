{
  const ready = () => {
    // "Show log" links in "Updates" page
    let links = document.querySelectorAll('a.log');
    for (let i = 0; i < links.length; i += 1) {
      const el = links[i];
      el.addEventListener('click', (e) => {
        e.target.parentElement.querySelector('div.log').classList.toggle('hide');
        e.preventDefault();
      });
    }

    // "Travis data" links
    links = document.querySelectorAll('a.travis');
    for (let i = 0; i < links.length; i += 1) {
      const el = links[i];
      el.addEventListener('click', (e) => {
        e.target.parentElement.querySelector('div.travis_raw').classList.toggle('hide');
        e.preventDefault();
      });
    }
  };
  if (document.readyState === 'complete' || document.readyState !== 'loading') {
    ready();
  } else {
    document.addEventListener('DOMContentLoaded', ready);
  }
}
