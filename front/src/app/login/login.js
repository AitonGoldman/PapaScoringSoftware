angular.module('app.login',[/*REPLACEMECHILD*/]);
angular.module('app.login').controller(
    'app.login',['$scope','$state','TimeoutResources','Utils',
                 function($scope, $state, TimeoutResources,Utils) {
                     $scope.site=$state.params.site;
                     $scope.process_step=$state.params.process_step;
      }]        
);


