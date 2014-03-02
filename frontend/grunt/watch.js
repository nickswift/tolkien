module.exports = {
    livereload: { 
        options: {
            livereload: '<%= connect.options.livereload %>'
        },
        files: [
            'src/{,*/}*.html',
            '{.tmp, src}/js/{,*/}*.js'
        ]
    }
};