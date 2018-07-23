angular.module('app.results.finals.final',['app.results.finals.final.round',
    /*REPLACEMECHILD*/]);
angular.module('app.results.finals.final').controller(
    'app.results.finals.final',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
	$scope.division_final_id=$state.params.division_final_id;
        finals_promise = TimeoutResources.GetDivisionFinals($scope.bootstrap_promise,{site:$scope.site});        
        // = TimeoutResources.GetEtcData();
        finals_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();            
            $scope.rounds_length = $scope.resources.finals.data[$scope.division_final_id].division_final_rounds.length;            
            console.log($scope.rounds_length);
        });
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
