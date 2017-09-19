import ReconnectingWebSocket from 'reconnecting-websocket';

/**
 * Bridge between Channels and plain javascript.
 *
 * @example
 * const webSocketBridge = new WebSocketBridge();
 * webSocketBridge.connect();
 * webSocketBridge.listen(function(action, stream) {
 *   console.log(action, stream);
 * });
 */
// export default
class API {
  constructor(options) {
    /**
     * The underlaying `ReconnectingWebSocket` instance.
     *
     * @type {ReconnectingWebSocket}
     */
    // this.defaultStream = stream;
    this.socket = null;
    this.streams = {};
    this.default_cb = null;
    this.options = { ...options };
    this.connect();
    this.listen((action, stream) => {
      console.log(`Unknown stream ${stream}`);
    });
  }

  /**
   * Connect to the websocket server
   *
   * @param      {String}  [url]     The url of the websocket. Defaults to
   * `window.location.host`
   * @param      {String[]|String}  [protocols] Optional string or array of protocols.
   * @param      {Object} options Object of options for [`reconnecting-websocket`](https://github.com/joewalnes/reconnecting-websocket#options-1).
   * @example
   * const webSocketBridge = new WebSocketBridge();
   * webSocketBridge.connect();
   */
  connect(url, protocols, options) {
    let u;
    // Use wss:// if running on https://
    const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const baseUrl = `${scheme}://${window.location.host}`;
    if (url === undefined) {
      u = baseUrl;
    } else if (url[0] === '/') { // Support relative URLs
      u = `${baseUrl}${url}`;
    } else {
      u = url;
    }
    this.socket = new ReconnectingWebSocket(u, protocols, options);
  }

  /**
   * Starts listening for messages on the websocket, demultiplexing if necessary.
   *
   * @param      {Function}  [cb]         Callback to be execute when a message
   * arrives. The callback will receive `action` and `stream` parameters
   *
   * @example
   * const webSocketBridge = new WebSocketBridge();
   * webSocketBridge.connect();
   * webSocketBridge.listen(function(action, stream) {
   *   console.log(action, stream);
   * });
   */
  listen(cb) {
    this.default_cb = cb;
    this.socket.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      console.log('MSG: ', msg);

      if (msg.stream !== undefined) {
        const { payload, stream } = msg;
        // stream = msg.stream;
        const callback = this.streams[stream];
        if (callback) {
          // callback(payload, stream);
          callback(payload);
        }
      } else {
        const action = msg;
        const stream = null;
        if (this.default_cb) {
          this.default_cb(action, stream);
        }
      }
    };
  }

  /**
   * Adds a 'stream handler' callback. Messages coming from the specified stream
   * will call the specified callback.
   *
   * @param      {String}    stream  The stream name
   * @param      {Function}  cb      Callback to be execute when a message
   * arrives. The callback will receive `action` and `stream` parameters.

   * @example
   * const webSocketBridge = new WebSocketBridge();
   * webSocketBridge.connect();
   * webSocketBridge.listen();
   * webSocketBridge.demultiplex('mystream', function(action, stream) {
   *   console.log(action, stream);
   * });
   * webSocketBridge.demultiplex('myotherstream', function(action, stream) {
   *   console.info(action, stream);
   * });
   */
  extend(stream, cb) {
    this.streams[stream] = cb;
  }

  /**
   * Sends a message to the reply channel.
   *
   * @param      {Object}  msg     The message
   *
   * @example
   * webSocketBridge.send({prop1: 'value1', prop2: 'value1'});
   */
  send(msg) {
    this.socket.send(JSON.stringify(msg));
  }

  // list() {
  //   this.stream(this.defaultStream).send({ action: 'list' });
  // }

  /**
   * Returns an object to send messages to a specific stream
   *
   * @param      {String}  stream  The stream name
   * @return     {Object}  convenience object to send messages to `stream`.
   * @example
   * webSocketBridge.stream('mystream').send({prop1: 'value1', prop2: 'value1'})
   */
  stream(stream) {
    return {
      send: (action) => {
        const msg = {
          stream,
          payload: action,
        };
        this.send(msg);
      },
      list: () => this.send({ stream, payload: { action: 'list' } }),
    };
  }
}
window.api = new API();
window.api.extend('courses', (payload) => {
  const {
    errors,
    data,
    action,
    response_status,
  } = payload;
  console.log(data);
});
window.courses = window.api.stream('courses');
// window.courses = new API('courses');

// {
//   const ready = () => {
// window.api = new API();
//   };

//   if (document.readyState === 'complete' || document.readyState !== 'loading') {
//     ready();
//   } else {
//     document.addEventListener('DOMContentLoaded', ready);
//   }
// }
