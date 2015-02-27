var gulp                = require('gulp')
var postcss             = require('gulp-postcss')
var autoprefixer        = require('autoprefixer-core')
var atImport            = require('postcss-import')
var customProperties    = require('postcss-custom-properties')
var fontVariants        = require('postcss-font-variant')
var customMedia         = require('postcss-custom-media')
var rename              = require('gulp-rename')
var minify              = require('gulp-minify-css')
var util                = require('gulp-util')


// Autoprefix and concatenate CSS styles
gulp.task('build', function () {
    var processors = [
        atImport(),
        fontVariants(),
        autoprefixer({ browsers: ['last 3 versions']}),
        customProperties(),
        customMedia()
    ];
    return gulp.src('./css/src/index.css')
        .pipe(postcss(processors))
        .pipe(gulp.dest('./css/'))
        .pipe(minify())
        .pipe(rename('index.min.css'))
        .pipe(gulp.dest('./css/'))
})

// Re-run build process on changes to CSS
gulp.task('watch', function () {
    gulp.watch('./css/src/*.css', ['build'])
})

// Register default task
gulp.task('default', ['watch'])
