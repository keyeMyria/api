// Watch files changes, restart services
var gulp = require('gulp')
var sass = require('gulp-sass')
var livereload = require('gulp-livereload')
var shell = require('gulp-shell')
// var sourcemaps = require('gulp-sourcemaps')
// var fs = require('fs')
// var path = require('path')
var exec = require('child_process').exec
var ts = require('gulp-typescript')
// var uglify = require('gulp-uglify')
// var buffer = require('gulp-buffer')
var browserify = require('browserify')
// var tap = require('gulp-tap')
// var gutil = require('gulp-util')
var transform = require('vinyl-transform')

// function get_apps(srcpath) {
// return fs.readdirSync(srcpath).filter(function(file) {
//  return fs.statSync(path.join(srcpath, file)).isDirectory() && file!=='__pycache__';
// });
// }

// settings.py
gulp.task('settings', function () {
  gulp.watch('src/**/settings*.jinja').on('change', function (info) {
    console.log(info.path)
    var output = info.path.substr(0, info.path.lastIndexOf('.'))
    console.log(output)
    exec('./configs/render.py ' + info.path, function (err, stdout, stderr) {
      console.log(stdout)
      console.log(stderr)
    })
    // exec('mustache /tmp/conf.json '+ info.path +' > ' + output, function (err, stdout, stderr) {
    // console.log(stdout);
    // console.log(stderr);
    // });
    livereload()
  })
})

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

// Processing SCSS
gulp.task('css', function () {
  return gulp.src('src/**/*.scss', {base: './'})
  // {base: "./"} - ?
    .pipe(sass())
    .pipe(gulp.dest('.', { ext: '.css' }))
    .pipe(livereload())
})

// Processing Javascript (Typescript actually)
gulp.task('scripts', function () {
    // var tsResult = gulp.src('src/**/*.ts')
    //     .pipe(ts({
    //         declaration: true
    //     }));
  // var browserified = transform(function (filename) {
  //   var b = browserify(filename)
  //   return b.bundle()
  // })

    // return merge([
    //     tsResult.dts.pipe(gulp.dest('release/definitions')),
    //     tsResult.js.pipe(gulp.dest('release/js'))
    // ]);
  return gulp.src('src/**/*.ts', {base: './'})
  // .pipe(sourcemaps.init())
    .pipe(ts({
      // declaration: true
      allowJs: true,
      lib: ['dom', 'es2016']
    }))
  // .pipe(tap(function (file) {
  //     gutil.log('bundling ' + file.path);

  //     // replace file contents with browserify's bundle stream
  //     file.contents = browserify(file.path, {debug: true}).bundle();

  // }))
  // .pipe(uglify())  // no need to minimize dev-version
  // .pipe(sourcemaps.write())
  // .pipe(browserified)
  // .pipe(gulp.dest('.', { ext: '.min.js' }))
    .pipe(livereload())
})

// gulp.task('js', function () {

//     return gulp.src('src/**/*.js', {read: false}) // no need of reading file because browserify does.

//     // transform file objects using gulp-tap plugin
//         .pipe(tap(function (file) {

//             gutil.log('bundling ' + file.path);

//             // replace file contents with browserify's bundle stream
//             file.contents = browserify(file.path, {debug: true}).bundle();

//         }))

//     // transform streaming contents into buffer contents (because gulp-sourcemaps does not support streaming contents)
//         .pipe(buffer())

//     // load and init sourcemaps
//         .pipe(sourcemaps.init({loadMaps: true}))

//         .pipe(uglify())

//     // write sourcemaps
//         .pipe(sourcemaps.write('./'))

//         .pipe(gulp.dest('dest'));

// });

// Reload when changing Jinja templates
gulp.watch('src/**/jinja2/*.jinja').on('change', livereload.changed)

// Watching .scss
gulp.task('scss', function () {
  gulp.watch('src/**/*.scss', ['css'])
})

// Watching .ts
gulp.task('ts', function () {
  gulp.watch('src/**/*.ts', ['scripts'])
})

// Start livereload server
gulp.task('livereload', function () {
  livereload.listen()
})

// The default task (called when you run `gulp` from cli)
// gulp.task('default', ['watch', 'scripts', 'images']);
gulp.task('default', [
  'livereload',
  'scss',
  'ts',
  'settings',
  'watch-secrets'
])
