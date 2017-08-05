angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function(    
    $stateProvider,
    $urlRouterProvider) {
    $urlRouterProvider.otherwise('/event_select');
    
    $stateProvider.state(
        'event_select', {
            cache:false,
            url: '/event_select',
            views: {
                '@': {
                    templateUrl: 'js/app/event_select.html',
                    controller: 'EventSelectController'

                },
                'e_select_view@event_select':{
                    templateUrl: 'js/app/e_select.html'
                }
            }
        }
    ).state(
        'app', {
            cache:false,
            url: '/:site/app',
            views: {
                '@': {
                    templateUrl: 'js/app/home.html',
                    controller: 'IndexController'
                },
                'menuContent@app': {
                    templateUrl: 'js/app/front.html',
                    controller: 'FrontController'
                }

            }
        }
    ).state(
        'app.redirect', {
            cache:false,
            url: '/redirect',
            views: {
                'menuContent@app': {
                    templateUrl: 'js/app/redirect.html',
                    controller: 'RedirectController'
                }

            }
        }
    ).state(
        'app.redirect_finals', {
            cache:false,
            url: '/redirect_finals',
            views: {
                'menuContent@app': {
                    templateUrl: 'js/app/redirect_finals.html',
                    controller: 'RedirectController'
                }

            }
        }
    ).state(
        'use_the_native_app', {
            url: '/use_the_native_app',
            views: {
                '@': {
                    templateUrl: 'js/app/use_the_native_app.html',
                    controller: 'NativeAppInstructionsController'
                    
                },
                'native_app_instructions@use_the_native_app':{
                    templateUrl: 'js/app/native_app_instructions.html'
                }
            }
        }
    );
}]);

