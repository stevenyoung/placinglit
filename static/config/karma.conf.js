module.exports = function(config) {
  config.set({
    // base path, that will be used to resolve files and exclude
    basePath: '../',

    frameworks: ['jasmine', 'requirejs'],

    // list of files / patterns to load in the browser
    files: [
      // !! Put all libs in RequireJS 'paths' config here (included: false).
      // All these files are files that are needed for the tests to run,
      // but Karma is being told explicitly to avoid loading them, as they
      // will be loaded by RequireJS when the main module is loaded.
      // all the sources, tests
      // !! all src and test modules (included: false)
      {pattern: 'app/scripts/vendor/*.js', included: false},
      {pattern: 'app/scripts/controllers/*.js', included: false},
      {pattern: 'app/scripts/directives/*.js', included: false},
      {pattern: 'app/scripts/filters/*.js', included: false},
      {pattern: 'app/scripts/services/*.js', included: false},
      {pattern: 'test/spec/controllers/*.js', included: false},
      {pattern: 'test/spec/directives/*.js', included: false},
      {pattern: 'test/spec/filters/*.js', included: false},
      {pattern: 'test/spec/services/*.js', included: false},

      // testing main require module last
      'test/spec/main.js'
    ],

    // list of files to exclude
    exclude: [

    ],


    // test results reporter to use
    // possible values: 'dots', 'progress', 'junit', 'growl', 'coverage'
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // Start these browsers, currently available:
    // - Chrome
    // - ChromeCanary
    // - Firefox
    // - Opera (has to be installed with `npm install karma-opera-launcher`)
    // - Safari (only Mac; has to be installed with `npm install karma-safari-launcher`)
    // - PhantomJS
    // - IE (only Windows; has to be installed with `npm install karma-ie-launcher`)
    browsers: ['PhantomJS'],


    // If browser does not capture in given timeout [ms], kill it
    captureTimeout: 60000,


    // Continuous Integration mode
    // if true, it capture browsers, run tests and exit
    singleRun: false
  });
};
