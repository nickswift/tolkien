/**
 * gruntfile copy task
 */
module.exports = {
    main: {
        expand: true,
        cwd   : 'src/',
        src   : '**/*.html',
        dest  : 'build/'
    },
    img: {
        expand: true,
        cwd   : 'src/',
        src   : 'res/img/**/*',
        dest  : 'build/'
    }
};