module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            build: {
                src: 'src/<%= pkg.name %>.js',
                dest: 'build/<%= pkg.name %>.min.js'
            }
        },
        watch: {
            js: {
                files: 'src/**/*.js',
                tasks: ['uglify']
            }
        },
        ngtemplates: {
            celery_task: {
                options: {
                    module: "Posting",
                },
                src: "web/templates/**/*.html",
                dest: "celery_task/static/js/app/templates.js"
            }
        }
    });
    grunt.registerTask('default', ['uglify']);
    grunt.loadTasks('grunt-angular-templates');
};