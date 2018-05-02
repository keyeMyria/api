/* eslint-disable no-console */

// Watch files changes, restart services
const gulp = require('gulp');
const sass = require('gulp-sass');
const livereload = require('gulp-livereload');
const shell = require('gulp-shell');
const sourcemaps = require('gulp-sourcemaps');
const source = require('vinyl-source-stream');
// const fs = require('fs');
// var path = require('path')
const exec = require('child_process').exec;
// const ts = require('gulp-typescript');
const rename = require('gulp-rename');
// var uglify = require('gulp-uglify')
// var buffer = require('gulp-buffer')
const buffer = require('vinyl-buffer');
const browserify = require('browserify');
// var tap = require('gulp-tap')
// var gutil = require('gulp-util')
// const transform = require('vinyl-transform');
// const babel = require('babel-core');
// const babel = require('gulp-babel');
// const writeFile = require('write');
const postcss = require('gulp-postcss');
const postcssimport = require('postcss-import');
// const csswring = require('csswring');
const postcssnested = require('postcss-nested');
// const syntax = require('postcss-scss');
const foreach = require('gulp-foreach');

// function get_apps(srcpath) {
// return fs.readdirSync(srcpath).filter(function(file) {
//  return fs.statSync(path.join(srcpath, file)).isDirectory() && file!=='__pycache__';
// });
// }

// settings.py
gulp.task('settings', () => {
  gulp.watch('src/**/settings*.jinja').on('change', (info) => {
    console.log(info.path);
    const output = info.path.substr(0, info.path.lastIndexOf('.')); // cut off ".jinja"
    console.log(output);
    exec(`./configs/render.py ${info.path}`, (err, stdout, stderr) => {
      console.log(stdout);
      console.log(stderr);
    });
    // exec('mustache /tmp/conf.json '+ info.path +' > ' + output, function (err, stdout, stderr) {
    // console.log(stdout);
    // console.log(stderr);
    // });
    livereload();
  });
});

// Change configuration if secret files changed
const secret = 'configs/secret*.json';
gulp.task(
  'secret',
  () => gulp.src(secret)
    .pipe(shell([
      'python configs/config.py configs/secret-example.json configs/secret.json',
    ]))
    .pipe(livereload()),
);
// Also update settings files
gulp.task('watch-secrets', () => {
  gulp.watch(secret, ['secret', 'settings']);
});

// ./config.py secret-example.json secret.json


// The default task (called when you run `gulp` from cli)
// gulp.task('default', ['watch', 'scripts', 'images']);
gulp.task('default', [
  'livereload',
  'settings',
  'watch-secrets',
]);
