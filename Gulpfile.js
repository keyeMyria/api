// Watch files changes, restart services
var gulp = require('gulp'),
    sass = require('gulp-sass'),
    livereload = require('gulp-livereload'),
    shell = require('gulp-shell'),
    sourcemaps = require('gulp-sourcemaps'),
	fs = require("fs"),
	path = require("path");

// settings.py
// var settings_template = 'configs/settings.py.mustache';
// gulp.task('settings.py', function() {
// 	return gulp.src(settings_template)
// 		.pipe(shell([
// 			'mustache s.json '+settings_template+' > src/pashinin/settings.py'
//         ]))
//         .pipe(livereload());
// });


// Processing SCSS
gulp.task('css', function() {
	return gulp.src('src/**/*.scss', {base: "./"})
		.pipe(sass())
		.pipe(gulp.dest('.', { ext: '.css' }))
		.pipe(livereload());
});

// Reload when changing Jinja templates
gulp.watch('src/**/jinja2/*.jinja').on('change', livereload.changed);

// Watching SCSS
gulp.task('scss', function() {
	gulp.watch('src/**/*.scss', ['css']);
});

// Start livereload server
gulp.task('livereload', function() {
	livereload.listen();
});


// The default task (called when you run `gulp` from cli)
//gulp.task('default', ['watch', 'scripts', 'images']);
gulp.task('default', [
	'livereload',
	'scss',
	'templates'
]);
