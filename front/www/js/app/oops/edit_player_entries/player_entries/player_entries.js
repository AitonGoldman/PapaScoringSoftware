angular.module('app.oops.edit_player_entries.player_entries',['app.oops.edit_player_entries.player_entries.select_division_machine',
    /*REPLACEMECHILD*/]);
angular.module('app.oops.edit_player_entries.player_entries').controller(
    'app.oops.edit_player_entries.player_entries',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;        
        $scope.utils = Utils;
        $scope.new_division_machine_id = $state.params.new_division_machine_id;
        $scope.new_division_machine_name = $state.params.new_division_machine_name;        
        $scope.new_entry = {division_machine_id:$scope.new_division_machine_id,score:undefined,division_machine_name:$scope.new_division_machine_name};        
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        player_entries_promise = TimeoutResources.GetPlayerEntries(undefined,{site:$scope.site,player_id:$scope.player_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        player_entries_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
        $scope.change_score = function(score){
            change_score_promise = TimeoutResources.SetScore(undefined,{site:$scope.site,score_id:score.score_id,score:score.score});
            Modals.loading();
            // = TimeoutResources.GetEtcData();
            change_score_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
                score.changed=true;
            });            
        };
        $scope.void_entry = function(entry,voided){
            void_entry_promise = TimeoutResources.VoidEntry(undefined,{site:$scope.site,entry_id:entry.entry_id,void:voided});
            Modals.loading();
            // = TimeoutResources.GetEtcData();
            void_entry_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
                if(voided == 1){
                    entry.voided=true;
                } else {
                    entry.voided=false;
                }                
            });            
        };
        $scope.add_entry = function(new_entry){
            console.log(new_entry);
            add_entry_promise = TimeoutResources.AddEntry(undefined,{site:$scope.site,player_id:$scope.player_id,division_machine_id:new_entry.division_machine_id,score:new_entry.score});
            Modals.loading();
            // = TimeoutResources.GetEtcData();
            add_entry_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
                console.log($scope.resources);
                $scope.resources.player_entries.data[0]={
                    score:{division_machine_name:$scope.new_division_machine_name,score:new_entry.score},
                    entry_id:$scope.resources.entry_added.data                    
                };
                new_entry.score=undefined;
                new_entry.division_machine_id=undefined;
                new_entry.division_machine_name=undefined;                                
            });            
        };                
    }]
);
