/* global $ */

$(document).ready(() => {
  // var url = $("form.api").attr("action");
  const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const wsPath = `${wsScheme}://${window.location.host}/admin/celery`;
  const ws = new WebSocket(wsPath);
  ws.onopen = () => {
    // console.log('websocket connected');
    $('#log').val('');
  };
  ws.onmessage = (e) => {
    const data = JSON.parse(e.data);
    // let stream = data['s']  // stream
    const d = data.p; // payload
    // console.log(e.data);
    try {
      $('#log').val($('#log').val() + d.logline);
    } catch (err) {
      // обработка ошибки
    }
  };
  ws.onerror = () => {
    // console.error(e);
  };
  ws.onclose = () => {
    // console.log('connection closed');
  };

  $('a.task').each((i, el) => {
    $(el).click(() => {
      ws.send(JSON.stringify({
        p: {
          task: $(el).text(),
        },
        s: 'task',
      }));
      return false;
    });
  });

  $('a#run_celery').click(() => {
    ws.send(JSON.stringify({ p: { key: 'value' }, s: '' }));
    // ws.send(JSON.stringify({"payload": {"key": "value"}, "stream": "0"}));
    // $.ajax({
    // type: 'POST',
    // url: $(this).attr('href'),
    // data: {'start':true},
    // context: this,
    // dataType: 'json',
    // success: function(d){
    // // location.reload();
    // console.log(d);
    // }
    // });
    return false;
  });
});
