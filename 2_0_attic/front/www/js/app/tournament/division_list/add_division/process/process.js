angular.module('app.tournament.division_list.add_division.process',[/*REPLACEMECHILD*/]);
angular.module('app.tournament.division_list.add_division.process').controller(
    'app.tournament.division_list.add_division.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.tournament_id=$state.params.tournament_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.division_info=$state.params.division_info;
     
        Modals.loading();
        add_division_promise = TimeoutResources.AddDivision($scope.bootstrap_promise,{site:$scope.site},$scope.division_info);
        // = TimeoutResources.GetEtcData();
        add_division_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
    }]
);
