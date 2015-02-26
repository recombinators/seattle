__To run the CSS build script:__

Install [NPM](https://www.npmjs.com/) with Homebrew:

```
brew install node
```

In the current directory, install the packages with NPM.

```
npm install .
```

Run gulp.

```
gulp
```

Once started, Gulp will watch for any changes to the css in `/src`, and will
rebuild (concatenate and minify) the CSS.
