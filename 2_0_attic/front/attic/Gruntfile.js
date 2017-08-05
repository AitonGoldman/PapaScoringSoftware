module.exports = function(grunt) {
    var dest = '/var/www/html/'
    var admin_dest = '/var/www/html/dist_2/'
    var player_dest = '/var/www/html/player/'    
    var backend_ip = grunt.option('backend_ip') || undefined;
    var secure = grunt.option('secure') || false;

    if(secure == true){
        player_protocol="https";
    } else {
        player_protocol="http";
    }
    
    if(backend_ip == undefined){
        console.log('OOPS!  No backend ip was specified.');
        console.log('Usage : grunt --backend_ip=<backend ip>');
        return;
    }
    
    grunt.initConfig({
        shell: {
	    makeRevHistory: {
		command: ["git log --pretty=format:'%H<msgst>%b<msge>' | fgrep -v '<msgst><msge>' | fgrep '<msgst>' | cut -b1-40 | git log --stdin --no-walk > "+admin_dest+"rev.txt",
			  "echo '<pre>' > "+admin_dest+"rev.html",
			  "cat "+admin_dest+"rev.txt >> "+admin_dest+"rev.html",
			  "echo '<pre>' >> "+admin_dest+"rev.html"
			 ].join('&&')
	    }
        },
        pkg: [grunt.file.readJSON('package.json')],
        clean: {
	    options: {'force':true},
	    TDApp: [admin_dest]            
        },
        prettify: {
            TDApp: {
                expand: true,
                src: ['html/**/*.html'],
                overwrite: true,
                options: {
                    indent: 1,
                    indent_char: '	',
                },
            },
        },
	ngtemplates: {
	    TDApp: {
		cwd: 'src',
		src: '**/**.html',
		dest: admin_dest+'app_html_templates.js'
	    }
	},
        browserify: {
            TDApp: {
                options: {
                    browserifyOptions: {
                        //debug: true,
                    },
                    transform: ['browserify-ngannotate'],
                },
                src: 'src/app/app.js',                
                dest: admin_dest+'js/app.js',
            }
        },        
        compass: {
            TDApp: {
                options: {
                    sassDir: 'styles',
                    cssDir: admin_dest+'css',
                    importPath: 'node_modules'
                },
            }            
        },
        copy: {
            TDApp: {
                files : [
                    { expand: true, cwd: 'img/', src: '**', dest: admin_dest+'img/' },
                    { expand: true, cwd: 'src/app/', src: 'index.html', dest: admin_dest },		    
                    {
                        expand: true,
                        cwd: 'node_modules/bootstrap-sass/assets/fonts/bootstrap/',
                        src: '*',
                        dest: admin_dest+'bootstrap/'
                    },
                    {
                        expand: true,
                        cwd: 'thirdparty/js',
                        src: '*',
                        dest: admin_dest+'thirdparty/js/'
                    },
                                        {
                        expand: true,
                        cwd: 'thirdparty/css',
                        src: '*',
                        dest: admin_dest+'thirdparty/css/'
                    },                    
                    {
                        expand: true,
                        cwd: 'bower_components/mobile-angular-ui/dist/fonts/',
                        src: '*',
                        dest: admin_dest+'fonts'
                    }		    
                ]
            }
        },
        concat: {
            TDApp: {
                src:[
                    admin_dest+'js/app.js',
                    admin_dest+'thirdparty/js/*.js',
                    'src/app/**/*.js',
                    '!src/app/app.js',
                    'src/services/**.js',
                    'src/app/routes.js',
                    admin_dest+'app_html_templates.js'                    
                ],
                dest: admin_dest+'js/app.concat.js'
            }
        },
        bower_concat: {
	    TDApp: {
		dest: {
		    'js': admin_dest+'js/_bower.js',
		    'css': admin_dest+'css/_bower.css'
		},
		bowerOptions: {
		    relative: false
		}
	    }
        },
        uglify: {          
          options: {
              mangle:true,              
              reserveDOMCache: true,
              nameCache: '/tmp/grunt-uglify-cache.json'
          },
            TDApp: {                
                files: [
                    {
                        '/var/www/html/dist_2/js/app.min.js': [admin_dest+'js/app.concat.js']
                    },
                    {
                        '/var/www/html/dist_2/js/_bower.min.js': [admin_dest+'js/_bower.js']
                    },
                ]
            }
        },
        replace: {
            TDApp: {
                src: [admin_dest+'js/app.min.js', admin_dest+'**/*html'],
                overwrite: true,
                replacements: [
                    {
                        from: '[APIHOST]',
                        to: 'http://'+backend_ip+':8000'
                    },
                ]
            }            
        },
        watch: {
            main: {		
                files: ['src/**/*',  'styles/**/*'],
                tasks: ['default'],
                options: {
                    livereload: true
                }
            }
        },
        rename: {
            player: {
                files: [
  		    {src: [player_dest+'player.html'], dest: player_dest+'index.html'},
                ]
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-rename');
    grunt.loadNpmTasks('grunt-contrib-copy');    
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-shell');
    grunt.loadNpmTasks('grunt-text-replace');
    grunt.loadNpmTasks('grunt-prettify');
    grunt.loadNpmTasks('grunt-angular-templates');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-bower-concat');    
    grunt.registerTask('admin_build', [
	'clean:TDApp',
        'compass:TDApp',        
        'browserify:TDApp',
	'ngtemplates:TDApp',
        'concat:TDApp',
	'bower_concat:TDApp',
        'uglify:TDApp',                 
        'copy:TDApp',
        'replace:TDApp',
	'shell:makeRevHistory'
    ]);

    grunt.registerTask('default', [
        'admin_build',
        'replace:TDApp'        
    ]);
};
