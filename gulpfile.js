var gulp = require('gulp'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    pump = require('pump');

gulp.task('frontend:plugins', function(cb) {
    pump([
        gulp.src('src/frontend/plugins/*.js'),
        concat('plugins.js'),
        gulp.dest('src/toja/static')
    ], cb);
});

gulp.task('frontend', gulp.parallel('frontend:plugins'));

gulp.task('theme:static', function(cb) {
    pump([
        gulp.src('src/theme/static/**/*.*'),
        gulp.dest('src/toja/static')
    ], cb);
});

gulp.task('theme:styles', function(cb) {
    pump([
        gulp.src([
            'src/theme/fonts.scss',
            'src/theme/app.scss'
        ]),
        sass({
            includePaths: ['node_modules/foundation-sites/scss']
        }),
        autoprefixer({
            cascade: false
        }),
        concat('theme.css'),
        gulp.dest('src/toja/static/')
    ], cb);
});

gulp.task('theme', gulp.parallel('theme:static', 'theme:styles'));

/*gulp.task('frontend', function(cb) {
    pump([
        gulp.src([
            'node_modules/fabricjs/index.js',
            'src/frontend/*.js'
        ]),
        concat('frontend.js'),
        gulp.dest('src/toja/static/')
    ], cb);
});*/

gulp.task('default', gulp.parallel('theme', 'frontend'));

gulp.task('watch', gulp.series('default', function(cb) {
    gulp.watch('src/theme/**/*.scss', gulp.series('theme:styles'));
    gulp.watch('src/frontend/plugins/**/*.js', gulp.series('frontend:plugins'));
    cb();
}));
