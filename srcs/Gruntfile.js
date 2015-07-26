module.exports = function (grunt) {
    grunt.initConfig({
        less: {
            css: {
                files: {"css/style.css": "css/style.less"},
                options: {
                    sourceMap: true,
                    sourceMapURL: '../css/style.css.map',
                    sourceMapFilename: 'css/style.css.map'
                }
            },
            theme: {
                files: {"theme/bootstrap-theme.css": "theme/bootstrap-theme.less"},
                options: {
                    sourceMap: true,
                    sourceMapURL: '../theme/bootstrap-theme.css.map',
                    sourceMapFilename: 'theme/bootstrap-theme.css.map'
                }
            }
        },
        watch: {
            options: {
                livereload: true
            },
            less: {
                files: ["theme/*.less", "css/*.less"],
                tasks: ['less']
            },
            html: {
                files: ["index.html"]
            }
        },
        connect: {
            server: {
                options: {
                    hostname: 'localhost',
                    port: 9005
                }
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-connect');

    grunt.registerTask('default', ['less', 'connect', 'watch']);
};

