angular.module('pss').config(['$stateProvider', '$urlRouterProvider',function($stateProvider,$urlRouterProvider) {
    $urlRouterProvider.otherwise('/event_select');
    $stateProvider.state(
        'event_select', {
            url:'/event_select',
            templateUrl:'templates/event_select.html',
            controller: 'event_select_controller'            
        }
    );}]);
