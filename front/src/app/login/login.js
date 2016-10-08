angular.module('app.login',['app.login.process'/*REPLACEMECHILD*/]);
angular.module('app.login').controller(
    'app.login',['$scope','$state','TimeoutResources',
                 function($scope, $state, TimeoutResources) {
                     $scope.site=$state.params.site;
                     $scope.process_step=$state.params.process_step;
                     //mylodash.size($scope.process_step);                                          
      }]        
);


