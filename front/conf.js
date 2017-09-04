exports.config = {
    framework: 'jasmine',
    seleniumAddress: 'http://localhost:4444/wd/hub',    
    suites: {
        experiment: 'specs/experiment/*.js',
        all: 'specs/**/*.js'
    }    
}
