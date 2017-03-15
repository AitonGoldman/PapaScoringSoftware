angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function(    
    $stateProvider,
    $urlRouterProvider) {
    $urlRouterProvider.otherwise('/event_select');
    
    $stateProvider.state(
        'event_select', {
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
            url: '/:site/app',
            views: {
                '@': {
                    templateUrl: 'js/app/home.html',
                    controller: 'IndexController'
                },
                'menuContent@app': {
                    templateUrl: 'js/app/front.html'                    
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

