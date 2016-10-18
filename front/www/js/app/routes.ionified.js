angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function(    
    $stateProvider,
    $urlRouterProvider) {    
    $urlRouterProvider.otherwise('/enter');
    
    $stateProvider.state(
        'enter', {
            url: '/enter',            
            templateUrl: 'js/app/enter.html'            
        }
    ).state(
        'app', {
            cache: false,
            url: '/:site/app',
            views: {
                '@' : {
                    templateUrl: 'js/app/home.html',
                    controller: 'IndexController'                     
                },
                'menuContent@app': {
                    templateUrl: 'js/app/front.html'                    
                }
            }            
        }
    ).state(
        'app.login', {
            cache: false,            
            url: '/login',
            views: {
                'menuContent': {
                    templateUrl: 'js/app/login/login.html',
                    controller: 'app.login'
                    
                }
            }            
        }
    ).state(
        'app.login.process', {
            cache: false,
            url: '/process',
            views: {
                'menuContent@app': {
                    templateUrl: 'js/app/login/process/process.html',
                    controller: 'app.login.process'

                }
            },
            params : {
                process_step:{},
                user_info:{}
            }
        }
    );
}]);

