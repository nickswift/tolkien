/**
 * Tolkien frontend gruntfile
 */

module.exports = function(grunt){

    var path = require('path');

    require('load-grunt-tasks')(grunt);
    require('load-grunt-config')(grunt, {
        configPath: path.join(process.cwd(), 'grunt'),
        init: true,
        config: { 
            test: false
        }
    });

    grunt.registerTask('default', [
        'jshint',
        'useminPrepare',
        'concat',
        'uglify',
        'cssmin',
        'copy',
        'usemin'
    ]);
};