angular.module('app.login',['app.login.process',/*REPLACEMECHILD*/]);
angular.module('app.login').controller(
    'app.login',['$scope','$state','TimeoutResources','Utils','Modals','User',
                 function($scope, $state, TimeoutResources,Utils,Modals,User) {
                     $scope.utils = Utils;
                     $scope.user = {};
                     $scope.utils.controller_bootstrap($scope,$state);
                 }]        
);




