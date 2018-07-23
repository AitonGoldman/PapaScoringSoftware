angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function(    
    $stateProvider,
    $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    
    $stateProvider.state(
        'event_select', {
            url: '/',
            views: {
                '@': {
                    templateUrl: 'app/event_select.html'//,
                    //controller: 'EventSelectController'
                },
                'title@':{
                    template: 'Event Select'
                },                
                'backbutton@':{
                    template: " "
                }
            }
        }).state(
        'app', {
            url: '/:site/app',
            views: {
                '@': {
                    templateUrl: 'app/home.html',
                    controller: 'IndexController'
                },
                'title@':{
                    template: 'TD Home'
                },                
                'backbutton@':{
                    template: " "
                }
            }
        }).state(
        'app.test', {
            url: '/:site/test',
            views: {
                '@': {
                    templateUrl: 'app/test.html',
                    controller: 'TestController'
                },
                'title@':{
                    template: ' test poop '
                },
                'backbutton@':{
                    template: "<md-button ng-click='back()' ng-controller='BackButtonController'><md-icon md-font-set='material-icons'> navigate_before </md-icon></md-button>"
                }
            }
        });
}]);

