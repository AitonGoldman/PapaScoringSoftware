angular.module('app.scorekeeping.machine_select.player_select.process',[/*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.player_select.process').controller(
    'app.scorekeeping.machine_select.player_select.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicHistory) {
            $ionicHistory.nextViewOptions({disableBack:true});            

            $scope.site=$state.params.site;
	    $scope.division_id=$state.params.division_id;
	    $scope.player_id=$state.params.player_id;
	    $scope.previous_player_id=$state.params.previous_player_id;
	    $scope.previous_player_name=$state.params.previous_player_name;            
	    $scope.division_machine_id=$state.params.division_machine_id;
	    $scope.division_machine_name=$state.params.division_machine_name;
            
            $scope.existing_queue_machine=$state.params.existing_queue_machine;
            
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            $scope.process_step=$state.params.process_step;
            if(_.size($scope.process_step)==0){
                //Utils.stop_post_reload();
                Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
                return;
            }
            
            $scope.player_info=$state.params.player_info;
            $scope.team_id=$scope.player_info.team_id;
            $scope.from_queue=$state.params.from_queue;
            $scope.add_team_to_machine_process_function = function(){
                Modals.loading();
                add_team_to_machine_promise = TimeoutResources.AddTeamToMachine($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id,division_machine_id:$scope.division_machine_id,team_id:$scope.team_id});
                
                add_team_to_machine_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    $scope.team_tournament = $scope.resources.divisions.data[$scope.division_id].team_tournament;
                    //console.log($scope.resources);
                    Modals.loaded();
        });                    

            };

            $scope.add_player_to_machine_process_function = function(){
                Modals.loading();
                $scope.existing_queue_machine=undefined;                
                $scope.existing_queue_machine_confirmed=true;
                if($scope.from_queue == 0){
                    add_player_to_machine_promise = TimeoutResources.AddPlayerToMachine($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id,division_machine_id:$scope.division_machine_id,player_id:$scope.player_info.player_id});
                    //= TimeoutResources.GetEtcData();
                    add_player_to_machine_promise.then(function(data){
                        $scope.resources = TimeoutResources.GetAllResources();
                        $scope.team_tournament = $scope.resources.divisions.data[$scope.division_id].team_tournament;
                        console.log($scope.resources);
                        Modals.loaded();
                    });            
                }
                if($scope.from_queue == 1){
                    add_player_to_machine_promise = TimeoutResources.AddPlayerToMachineFromQueue($scope.bootstrap_promise,{site:$scope.site,division_machine_id:$scope.division_machine_id});
                    //= TimeoutResources.GetEtcData();
                    add_player_to_machine_promise.then(function(data){
                        $scope.resources = TimeoutResources.GetAllResources();
                        $scope.team_tournament = $scope.resources.divisions.data[$scope.division_id].team_tournament;                        
                        console.log($scope.resources);
                        Modals.loaded();
                    });            
                }
            };            
            if($scope.existing_queue_machine == undefined||$scope.existing_queue_machine == ""){
                $scope.resources = TimeoutResources.GetAllResources();                
                if($scope.resources.divisions.data[$scope.division_id].team_tournament!=true){
                    $scope.add_player_to_machine_process_function();
                } else {
                    $scope.add_team_to_machine_process_function();                    
                }
                
            }
        }]
);
