// Watch files changes, restart services
var gulp = require('gulp'),
    sass = require('gulp-sass'),
    livereload = require('gulp-livereload'),
    shell = require('gulp-shell'),
    sourcemaps = require('gulp-sourcemaps'),
	fs = require("fs"),
	path = require("path");

// settings.py
var settings_template = 'configs/settings.py.mustache';
gulp.task('settings.py', function() {
	return gulp.src(settings_template)
		.pipe(shell([
			'mustache /tmp/conf.json '+settings_template+' > src/pashinin/settings.py'
        ]))
        .pipe(livereload());
});
gulp.task('settings', function() {
	gulp.watch(settings_template, ['settings.py']);
});


// config data (secret files)
var secret = 'configs/secret.json';
gulp.task('secret', function() {
	return gulp.src(secret)
		.pipe(shell([
			'python configs/config.py configs/secret-example.json configs/secret.json'
        ]))
        .pipe(livereload());
});
gulp.task('watch-secrets', function() {
	gulp.watch(secret, ['secret', 'settings']);
});


// ./config.py secret-example.json secret.json


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
	'settings',
	'watch-secrets'
]);
