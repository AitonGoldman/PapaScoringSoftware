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
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            Modals.loading();
            divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});
            player_promise = TimeoutResources.GetPlayer(divisions_promise,{site:$scope.site,player_id:$scope.player_id});
            
            // = TimeoutResources.GetEtcData();
            player_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.main_divisions = _.filter($scope.resources.divisions.data, { 'single_division': false});
                $scope.player_info = $scope.resources.player.data;
                $scope.player_info.old_linked_division_id = $scope.player_info.linked_division_id;                
                Modals.loaded();
            });
            $scope.on_div_change=function(){
                if($scope.player_info.linked_division_id != $scope.player_info.old_linked_division_id){
                    ActionSheets.choose_change_div($scope.player_info);
                }
            };
        }]
);
