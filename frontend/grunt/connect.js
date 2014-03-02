/**
 * A simple static file server that allows frontend development without 
 * necessitating configuration of a fully featured one like Apache
 */
module.exports = {
    options: {
        port       : 9000,
        hostname   : 'localhost',
        livereload : 35729
    },
    livereload:{ 
        options: {
            open: true,
            base: [
                '.tmp',
                'src'
            ]
        }
    }
};