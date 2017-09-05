module.exports = {
  'root': true,
  // 'extends': 'google',

  // https://github.com/airbnb/javascript
  'extends': 'airbnb-base',  // without react
  // 'extends': 'airbnb',    // for react

  // 'extends': 'standard',
  // "parser": "babel-eslint",
  'env': {
    'browser': true,
    'es6': true
  },
  'plugins': [
    // 'standard',
    // 'promise'
  ],
  'rules': {
    // 'semi': 2
    // 'quote-props': ['error', 'always']
    'no-alert': 0
  }
}
