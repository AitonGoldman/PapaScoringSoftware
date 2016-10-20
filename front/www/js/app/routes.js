angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function(    
    $stateProvider,
    $urlRouterProvider) {
    $urlRouterProvider.otherwise('/poop/app');
    
    $stateProvider.state(
        'event_select', {
            url: '/event_select',
            templateUrl: 'js/app/event_select.html'
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
    );
}]);

