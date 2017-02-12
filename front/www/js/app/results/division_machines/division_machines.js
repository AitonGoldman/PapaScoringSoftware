angular.module('app.results.division_machines',['app.results.division_machines.machines',
    /*REPLACEMECHILD*/]);
angular.module('app.results.division_machines').controller(
    'app.results.division_machines',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.bootstrap_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
          $scope.divisions_to_display = _.filter($scope.resources.divisions.data, function(value,key) { console.log(value);console.log(key);return key!="metadivisions"; });
  
            Modals.loaded();
        });             
    }]
);
