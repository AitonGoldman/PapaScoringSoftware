angular.module('app.player.add_player.process',[/*REPLACEMECHILD*/]);
angular.module('app.player.add_player.process').controller(
    'app.player.add_player.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        Modals.loading();        
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.player_info=$state.params.player_info;
        if($scope.player_info.ifpa_result.result != undefined){
            $scope.player_info.ifpa_ranking=$scope.player_info.ifpa_result.result.wppr_rank;
            $scope.player_info.ifpa_result=undefined;
        } else {
            $scope.player_info.ifpa_ranking=999999;
        }
        player_add_promise = TimeoutResources.AddPlayer($scope.bootstrap_promise,{site:$scope.site},$scope.player_info);
        // = TimeoutResources.GetEtcData();
        player_add_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
