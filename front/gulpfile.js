var gulp = require('gulp');
var gutil = require('gulp-util');
var bower = require('bower');
var concat = require('gulp-concat');
var sass = require('gulp-sass');
var minifyCss = require('gulp-minify-css');
var rename = require('gulp-rename');
var sh = require('shelljs');
var karma = require('karma').server;
var Server = require('karma').Server;
var protractor = require("gulp-protractor").protractor;
var argv = require('yargs').argv;
//var replace = require('gulp-replace');
var replace = require('gulp-string-replace');

var paths = {
  sass: ['./scss/**/*.scss']
};

gulp.task('default', ['api_host_replace','sass']);

gulp.task('api_host_replace', function(done){
    if(argv.backend_ip == undefined){        
        done('--backend_ip argument needed!');
        return;
    }
    gulp.src(['./www/templates/api_host.js'])
        .pipe(replace('APIHOST', argv.backend_ip))
        .pipe(gulp.dest('./www/js/services'));
    done();
});

gulp.task('e2e', function(done) {
    if(argv.test_instance_ip == undefined){
        done('--test_instance_ip argument needed!');
        return;
    }
    var args = ['--params.test_instance_ip',argv.test_instance_ip];
    gulp.src(["./tests/*.js"])
        .pipe(protractor({
            configFile: "tests/config.js",
            args: args
        }))
        .on('error', function(e) { throw e; });
    done();
});

gulp.task('unit', function (done) {
    server = new Server({
         configFile: __dirname + '/karma.conf.js',
         singleRun: true
    }, done).start();
    
    // karma.start({
    //     configFile: __dirname + '/karma.conf.js',
    //     singleRun: true
    // }, done);
});

gulp.task('sass', function(done) {
  gulp.src('./scss/ionic.app.scss')
    .pipe(sass())
    .on('error', sass.logError)
    .pipe(gulp.dest('./www/css/'))
    .pipe(minifyCss({
      keepSpecialComments: 0
    }))
    .pipe(rename({ extname: '.min.css' }))
    .pipe(gulp.dest('./www/css/'))
    .on('end', done);
});

gulp.task('watch', function() {
    console.log('hi there');
    gulp.watch(paths.sass, ['sass']);
});

gulp.task('install', ['git-check'], function() {
  return bower.commands.install()
    .on('log', function(data) {
      gutil.log('bower', gutil.colors.cyan(data.id), data.message);
    });
});

gulp.task('git-check', function(done) {
  if (!sh.which('git')) {
    console.log(
      '  ' + gutil.colors.red('Git is not installed.'),
      '\n  Git, the version control system, is required to download Ionic.',
      '\n  Download git here:', gutil.colors.cyan('http://git-scm.com/downloads') + '.',
      '\n  Once git is installed, run \'' + gutil.colors.cyan('gulp install') + '\' again.'
    );
    process.exit(1);
  }
  done();
});
