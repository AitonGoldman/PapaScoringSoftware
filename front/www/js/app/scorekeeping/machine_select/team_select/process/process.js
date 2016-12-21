angular.module('app.scorekeeping.machine_select.team_select.process',[/*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.team_select.process').controller(
    'app.scorekeeping.machine_select.team_select.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {        
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_id=$state.params.division_machine_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.team_info=$state.params.team_info;        
        Modals.loading();
        console.log($scope.team_info);
        add_team_to_machine_promise = TimeoutResources.AddTeamToMachine(undefined,{site:$scope.site,division_id:$scope.division_id,division_machine_id:$scope.division_machine_id,team_id:$scope.team_info.team_id});
        //= TimeoutResources.GetEtcData();
        add_team_to_machine_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            //console.log($scope.resources);
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
