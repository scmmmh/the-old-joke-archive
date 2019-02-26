var gulp = require('gulp'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    pump = require('pump');

gulp.task('theme', function(cb) {
    pump([
        gulp.src('src/theme/app.scss'),
        sass({
            includePaths: ['node_modules/foundation-sites/scss']
        }),
        autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }),
        concat('theme.css'),
        gulp.dest('src/toja/static/')
    ], cb);
});

gulp.task('frontend', function(cb) {
    pump([
        gulp.src('src/frontend/*.js'),
        concat('frontend.js'),
        gulp.dest('src/toja/static/')
    ], cb);
});

gulp.task('default', gulp.parallel('theme', 'frontend'));

gulp.task('watch', gulp.series('default', function(cb) {
    gulp.watch('src/theme/**/*.scss', gulp.series('theme'));
    gulp.watch('src/frontend/**/*.js', gulp.series('frontend'));
    cb();
}));
