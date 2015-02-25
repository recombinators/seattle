var gulp                = require('gulp')
var postcss             = require('gulp-postcss')
var autoprefixer        = require('autoprefixer-core')
var atImport            = require('postcss-import')
var customProperties    = require('postcss-custom-properties')
var fontVariants        = require('postcss-font-variant')
var customMedia         = require('postcss-custom-media')
var rename              = require('gulp-rename')
var minify              = require('gulp-minify-css')


// Autoprefix and concatenate CSS styles
gulp.task('build', function () {
    var processors = [
        atImport(),
        fontVariants(),
        autoprefixer({ browsers: ['last 3 versions']}),
        customProperties(),
        customMedia()
    ];
    return gulp.src('./seattle/seattle/static/css/src/index.css')
        .pipe(postcss(processors))
        .pipe(gulp.dest('./seattle/seattle/static/css/'))
        .pipe(minify())
        .pipe(rename('index.min.css'))
        .pipe(gulp.dest('./seattle/seattle/static/css/'))
})

// Re-run build process on changes to CSS
gulp.task('watch', function () {
    gulp.watch('./seattle/seattle/css/src/*.css', ['build'])
})

// Register default task
gulp.task('default', ['watch'])

// TODO Add: log of output files
