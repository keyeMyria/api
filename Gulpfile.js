// Watch files changes, restart services
var gulp = require('gulp'),
    sass = require('gulp-sass'),
    livereload = require('gulp-livereload'),
    shell = require('gulp-shell'),
    sourcemaps = require('gulp-sourcemaps'),
	fs = require("fs"),
	path = require("path");
var exec = require('child_process').exec;

// function get_apps(srcpath) {
// 	return fs.readdirSync(srcpath).filter(function(file) {
// 		return fs.statSync(path.join(srcpath, file)).isDirectory() && file!=='__pycache__';
// 	});
// }

// settings.py
gulp.task('settings', function() {
	gulp.watch('src/**/settings*.jinja').on("change", function (info) {
		console.log(info.path);
		var output = info.path.substr(0, info.path.lastIndexOf("."));
		console.log(output);
		exec('./configs/render.py ' + info.path, function (err, stdout, stderr) {
			console.log(stdout);
			console.log(stderr);
		});
		// exec('mustache /tmp/conf.json '+ info.path +' > ' + output, function (err, stdout, stderr) {
		// 	console.log(stdout);
		// 	console.log(stderr);
		// });
		livereload();
	});
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
