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

if(argv.help){
    console.log('--test_instance_ip <ip> (for e2e target)');
    console.log('--single_protractor_spec <path_to_spec_file> (for e2e target)');
    console.log('--test_stripe_sku <stripe_sku> (for tests that need stripe sku)');
    return;
}
gulp.task('default', ['sass']);

gulp.task('e2e', function(done) {
    if(argv.test_instance_ip == undefined){
        done('--test_instance_ip argument needed!');
        return;
    }
    var single_spec = argv.single_protractor_spec;
    if(single_spec == undefined){
        specs_to_run = "./tests/*.js";
    } else {
        specs_to_run = single_spec;
    }
    var args = ['--params.test_instance_ip',argv.test_instance_ip];
    if(argv.test_stripe_sku){
        args.push('--params.test_stripe_sku');
        args.push(argv.test_stripe_sku);
    }    
    gulp.src([specs_to_run])
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
