angular.module('app.tournament.division_list.edit_division.process',[/*REPLACEMECHILD*/]);
angular.module('app.tournament.division_list.edit_division.process').controller(
    'app.tournament.division_list.edit_division.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
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
        update_div_promise = TimeoutResources.UpdateDivision(undefined,{site:$scope.site,division_id:$scope.division_id},$scope.division_info);
        // = TimeoutResources.GetEtcData();
        update_div_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
     
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
