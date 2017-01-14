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
    );
}]);

