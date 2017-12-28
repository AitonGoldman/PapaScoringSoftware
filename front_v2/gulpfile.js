var gulp = require('gulp');
var fs = require("fs");
const replace = require('replace-in-file');
var p = require('./package.json');
var version = p.version;
gulp.task('alldone', function(){
    console.log('poop');
});

gulp.task('default', function() {
    var results = fs.readFileSync("./templates/custom-header-contents.html", "utf-8");    
    const changes = replace.sync({
        files: ['./src/pages/**/*.html'],
        from: /\<\!--\<bobo\>--\>[\w\W\n]+\<\!--\<\/bobo\>--\>/g,
        to: results
    });
    console.log(changes);          
});
