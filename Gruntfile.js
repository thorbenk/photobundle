module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            min: {
                files: grunt.file.expandMapping(['js/*.js'], 'dist/js/', {
                    flatten: true,
                    rename: function(destBase, destPath) {
                        return destBase+destPath.replace('.js', '.min.js');
                    }
                })
            }
        },
        cssmin: {
            dist: {
                files: grunt.file.expandMapping(['css/*.css'], 'dist/css/', {
                    flatten: true,
                    rename: function(destBase, destPath) {
                        return destBase+destPath.replace('.css', '.min.css');
                    }
                })
            }
        },
        copy: {
            img: {
                cwd: 'img',
                src: '*',
                dest: 'dist/img',
                expand: true
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-uglify')
    grunt.loadNpmTasks('grunt-contrib-cssmin')
    grunt.loadNpmTasks('grunt-contrib-copy')
    grunt.registerTask('default', ['uglify:min', 'cssmin:dist', 'copy:img'])
};
