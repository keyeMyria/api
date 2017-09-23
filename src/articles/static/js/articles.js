/* global api, moment */
class Drafts {

}

function showDrafts() {
  document.querySelector('#article-edit').classList.add('hide');
  document.querySelector('#article-list').classList.add('hide');
  document.querySelector('#drafts-list').classList.remove('hide');
}
function showArticles() {
  document.querySelector('#article-edit').classList.add('hide');
  document.querySelector('#article-list').classList.remove('hide');
  document.querySelector('#drafts-list').classList.add('hide');
}
function showEdit() {
  document.querySelector('#article-edit').classList.remove('hide');
  document.querySelector('#article-list').classList.add('hide');
  document.querySelector('#drafts-list').classList.add('hide');
}
// function makeArticle(data){

// }


/**
 * Callback, executed when article is created
 * @param {Object} article -
 */
function articleAdded(article) {
  const t = document.querySelector('#mytemplate');
  // const rendered = Mustache.render(t.innerHTML, article);
  const clone = document.importNode(t.content, true);
  // const $ = t.content.querySelector.bind(t.content);
  const $ = clone.querySelector.bind(clone);
  // title.setAttribute('href', article.url);
  const { url, title } = article;

  $('.title').href = url;
  // $('.article').className = '';
  $('.article').classList.add(`a${article.pk}`);
  $('.title').innerHTML = title;
  $('.pk').innerHTML = article.pk;
  $('#cut').innerHTML = article.cut_html;
  $('#read-article').href = url;

  const m = moment(article.added);
  // console.log(m.format());
  // console.log(m.clone().tz("Europe/London").format());
  // $('time').innerHTML = article.added;
  $('time').innerHTML = m.fromNow();
  // $('time').innerHTML = m.calendar();
  $('time').setAttribute('datetime', m.format());
  //
  $('time').setAttribute('title', m.format('Do MMMM YYYY HH:mm:ss'));
  // post__time

  // console.log(article.author, api.uid);
  if (article.author === api.uid) {
    $('.delete.btn').classList.remove('hide');
  } else {
    $('.delete.btn').classList.add('hide');
  }
  // $('.delete.btn').classList.add('hide');

  if (article.published) {
    $('.edit.btn').classList.add('hide');
  } else {
    $('a.draft').classList.remove('hide');
    $('.edit.btn').classList.remove('hide');
  }

  $('.edit.btn').addEventListener('click', () => {
    showEdit();
  });

  // window.time.render(clone.querySelectorAll('.timeago'));

  $('.delete.btn').addEventListener('click', (e) => {
    const id = parseInt(e.target.closest('div.article').querySelector('span.pk').innerHTML, 10);
    window.api.stream('articles').send({ action: 'delete', pk: id });
  });

  // const clone = document.importNode(t.content, true);
  // const clone = document.importNode(rendered, true);
  // clone.outerHTML = rendered;

  const alist = document.getElementById('article-list');
  if (article.published) {
    alist.insertBefore(clone, alist.firstChild);
  } else {
    document.getElementById('drafts-list').appendChild(clone);
  }
}

function buildDraftsPage(items) {
  const content = document.getElementById('drafts-list');
  if (items.length) {
    content.innerHTML = '';
    items.forEach((draft) => {
      articleAdded(draft);
    });
  } else {
    content.innerHTML = '<p>Нет опубликованных статей</p>';
  }
}


function articleDeleted(article) {
  const $ = document.querySelector.bind(document);
  let a = $(`div.a${article.pk}`);
  while (a) {
    a.remove();
    a = $(`div.a${article.pk}`);
  }
}


window.drafts = new Drafts();


{
  const $ = document.querySelector.bind(document);
  const stream = 'articles';
  window.api.extend(stream, (payload) => {
    const {
      // errors,
      data,
      action,
    } = payload;

    if (action === 'drafts') {
      const { count } = data;
      $('#drafts_count').innerHTML = count;
      buildDraftsPage(data.items);
    }

    const status = payload.response_status;
    if (status === 201) {
      // alert('Статья создана');
      showEdit();
    }

    //
    if (status === 200 && action === 'list') {
      // console.log('add bulk', data);
      if (data.length) {
        document.getElementById('article-list').innerHTML = '';
        data.forEach((a) => {
          articleAdded(a);
        });
      } else {
        document.getElementById('article-list').innerHTML = '<p>Нет опубликованных статей</p>';
      }
    }

    // status 'undefined' means this is a 'subscribe'-message
    if (status === undefined) {
      if (action === 'create') {
        articleAdded(data);
      } else if (action === 'delete') {
        articleDeleted(data);
      }
    }
  });

  const api = window.api.stream(stream);
  api.onopen(() => {
    api.list();

    api.send({
      action: 'subscribe',
      data: {
        action: 'create',
      },
    });
    api.send({
      action: 'subscribe',
      data: {
        action: 'delete',
      },
    });
    api.send({
      action: 'drafts',
      data: {},
    });
  });


  const ready = () => {
    const newArticleBtn = document.getElementById('new-article-btn');
    if (newArticleBtn) {
      newArticleBtn.addEventListener('click', (e) => {
        showEdit();
        e.stopPropagation();
        e.preventDefault();
      });
    }

    Array.from(document.querySelectorAll('.menu-item')).forEach((el) => {
      el.addEventListener('click', (e) => {
        Array.from(e.target.closest('.menu').querySelectorAll('.menu-item')).forEach((item) => {
          item.classList.remove('selected');
        });
        e.target.classList.add('selected');
      });
    });

    const showDraftsBtn = document.getElementById('showDrafts');
    if (showDraftsBtn) {
      showDraftsBtn.addEventListener('click', (e) => {
        showDrafts();
        e.preventDefault();
      });
    }
    const showArticlesBtn = $('#showArticles');
    if (showArticlesBtn) {
      showArticlesBtn.addEventListener('click', (e) => {
        showArticles();
        e.preventDefault();
      });
    }

    const saveArticleBtn = document.getElementById('save-article-btn');
    if (saveArticleBtn) {
      saveArticleBtn.addEventListener('click', (e) => {
        api.send({
          action: 'create',
          data: {
            title: 'test@example.com',
            password: 'password',
          },
          request_id: 'someid',
        });
        e.stopPropagation();
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
