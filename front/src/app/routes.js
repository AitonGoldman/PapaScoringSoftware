angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function(    
    $stateProvider,
    $urlRouterProvider) {
    $urlRouterProvider.otherwise('/app');
    
    $stateProvider.state(
        'app', {
            url: '/:site/app',
            views: {
                '@': {
                    templateUrl: 'app/home.html',
                    controller: 'IndexController'
                },
                'title@':{
                    template: ' poop '
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

