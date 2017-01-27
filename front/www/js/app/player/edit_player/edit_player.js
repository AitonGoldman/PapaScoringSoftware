angular.module('app.player.edit_player',['app.player.edit_player.process',
                                         /*REPLACEMECHILD*/]);
angular.module('app.player.edit_player').controller(
    'app.player.edit_player',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
            $scope.site=$state.params.site;
	    $scope.player_id=$state.params.player_id;
            $scope.ActionSheets = ActionSheets;
            $scope.utils = Utils;            
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                            
            //divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});
            player_promise = TimeoutResources.GetPlayer($scope.bootstrap_promise,{site:$scope.site,player_id:$scope.player_id});
            
            // = TimeoutResources.GetEtcData();
            player_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.player_info = $scope.resources.player.data;
                $scope.player_info.old_linked_division_id = $scope.player_info.linked_division_id;
                $scope.main_divisions = _.filter($scope.resources.divisions.data, { 'single_division': false});
                dev_info = ionic.Platform.device();            
                if (_.size(dev_info)!=0){
                    $scope.is_native=true;          
                }                                
                Modals.loaded();
            });
            $scope.on_div_change=function(){
                if($scope.player_info.linked_division_id != $scope.player_info.old_linked_division_id){
                    ActionSheets.choose_change_div($scope.player_info);
                }
            };
            $scope.disable_division_radio = function(division_id){
                division_name = $scope.resources.divisions.data[division_id].division_name;
                linked_division_name = $scope.resources.divisions.data[$scope.player_info.linked_division_id].division_name;
                if(division_name>linked_division_name){
                    return true;
                } else {
                    return false;
                }
                
                    //< resources.divisions.data[player_info.linked_division_id].division_name
            };
        }]
);
