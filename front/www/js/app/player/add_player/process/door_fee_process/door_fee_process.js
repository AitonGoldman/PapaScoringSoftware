angular.module('app.player.add_player.process.door_fee_process',[/*REPLACEMECHILD*/]);
angular.module('app.player.add_player.process.door_fee_process').controller(
    'app.player.add_player.process.door_fee_process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
        $scope.resources = TimeoutResources.GetAllResources();
        player_edit_promise = TimeoutResources.UpdatePlayer($scope.bootstrap_promise,{site:$scope.site,player_id:        $scope.resources.added_player.data.player_id},{active:true});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        player_edit_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
    }]
);
