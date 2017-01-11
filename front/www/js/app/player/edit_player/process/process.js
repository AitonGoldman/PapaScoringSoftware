angular.module('app.player.edit_player.process',[/*REPLACEMECHILD*/]);
angular.module('app.player.edit_player.process').controller(
    'app.player.edit_player.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.player_info=$state.params.player_info;
        update_player_promise = TimeoutResources.UpdatePlayer($scope.bootstrap_promise,{site:$scope.site,player_id:$scope.player_id},$scope.player_info);
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        update_player_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
