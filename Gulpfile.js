// Watch files changes, restart services
const gulp = require('gulp');
const sass = require('gulp-sass');
const livereload = require('gulp-livereload');
const shell = require('gulp-shell');
const sourcemaps = require('gulp-sourcemaps');
const source = require('vinyl-source-stream');
const fs = require('fs');
// var path = require('path')
const exec = require('child_process').exec;
const ts = require('gulp-typescript');
const rename = require('gulp-rename');
// var uglify = require('gulp-uglify')
// var buffer = require('gulp-buffer')
const buffer = require('vinyl-buffer');
const browserify = require('browserify');
// var tap = require('gulp-tap')
// var gutil = require('gulp-util')
const transform = require('vinyl-transform');
// const babel = require('babel-core');
const babel = require('gulp-babel');
const writeFile = require('write');
const postcss = require('gulp-postcss');
const postcssimport = require('postcss-import');
const csswring = require('csswring');
const postcssnested = require('postcss-nested')
const syntax = require('postcss-scss');
const foreach = require('gulp-foreach');

// function get_apps(srcpath) {
// return fs.readdirSync(srcpath).filter(function(file) {
//  return fs.statSync(path.join(srcpath, file)).isDirectory() && file!=='__pycache__';
// });
// }

// settings.py
gulp.task('settings', () => {
  gulp.watch('src/**/settings*.jinja').on('change', (info) => {
    console.log(info.path)
    var output = info.path.substr(0, info.path.lastIndexOf('.'))  // cut off ".jinja"
    console.log(output)
    exec('./configs/render.py ' + info.path, function (err, stdout, stderr) {
      console.log(stdout)
      console.log(stderr)
    })
    // exec('mustache /tmp/conf.json '+ info.path +' > ' + output, function (err, stdout, stderr) {
    // console.log(stdout);
    // console.log(stderr);
    // });
    livereload();
  });
});

// config data (secret files)
var secret = 'configs/secret.json'
gulp.task('secret', function () {
  return gulp.src(secret)
    .pipe(shell([
      'python configs/config.py configs/secret-example.json configs/secret.json'
    ]))
    .pipe(livereload())
})
gulp.task('watch-secrets', function () {
  gulp.watch(secret, ['secret', 'settings'])
})

// ./config.py secret-example.json secret.json

// Processing CSS
gulp.task('css', () => {
  return gulp.src('src/**/[^_]*.scss', { base: './' })
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: ['./node_modules'],
    }).on('error', sass.logError))
    .pipe(postcss([
      postcssimport,
      postcssnested,
      // csswring,
      // ], { parser: syntax }))
    ]))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('.', { ext: '.css' }))
    .pipe(livereload());
});

// Reload when changing Jinja templates
gulp.watch('src/**/jinja2/*.jinja').on('change', livereload.changed);

// Watching .scss
gulp.task('watch:css', () => {
  gulp.watch('src/**/*.scss', ['css']);
});


const processJS = (file) => {
  console.log(`Compiling JS File: ${file.path}`);
  // if (file.path.endsWith('api.js')) {
  // const output = `${file.path.substr(0, file.path.lastIndexOf('.'))}.min.js`;
  browserify([file.path], { debug: true })
    .transform('babelify')
    .bundle()
    .pipe(source(file.path))
    .pipe(buffer())
    .pipe(sourcemaps.init({ loadMaps: true }))
  // .pipe(babel())
  // .pipe(uglify())
    .pipe(sourcemaps.write())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest('./'))
    .pipe(livereload());
};


// Watching .js
// https://stackoverflow.com/questions/23247642/modify-file-in-place-same-dest-using-gulp-js-and-a-globbing-pattern
const jsFiles = ['src/**/*.js', '!src/**/*.min.*', '!src/**/*.mini.js', '!src/**/js/libs/**/*.js'];
gulp.task('watch:js', () => {
  // gulp.watch(['src/**/*.js', '!src/**/*.min.*'], ['scripts']);
  gulp.watch(jsFiles, { read: false }).on('change', processJS);
});
// if (info.path.endsWith('.min.js') || info.path.endsWith('.mini.js')) return;

// gulp js
// Compile JS in dev-mode (with source maps)
gulp.task('js', () => {
  gulp.src(jsFiles, { read: false })
    .pipe(foreach((stream, file) => {
      processJS(file);
      // console.log(file);
      return stream;
    }));
});

// Start livereload server
gulp.task('livereload', () => {
  livereload.listen();
});

// The default task (called when you run `gulp` from cli)
// gulp.task('default', ['watch', 'scripts', 'images']);
gulp.task('default', [
  'livereload',
  'watch:css',
  'watch:js',
  'settings',
  'watch-secrets',
]);
