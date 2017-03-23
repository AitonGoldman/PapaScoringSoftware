angular.module('app.prereg_complete.confirm.picture',[/*REPLACEMECHILD*/]);
angular.module('app.prereg_complete.confirm.picture').controller(
    'app.prereg_complete.confirm.picture',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_name=$state.params.player_name;
	$scope.player_id=$state.params.player_id;
        $scope.player_info = {};
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                

        $scope.update_player = function(){
            $scope.player_info={player_id:$scope.player_id,pic_file:$scope.player_info.pic_file};
            Modals.loading();
            update_player_promise = TimeoutResources.UpdatePlayer(undefined,{site:$scope.site,player_id:$scope.player_id},$scope.player_info);
            update_player_promise.then(function(data){
                Modals.loaded();
                $state.go('.^.process',{process_step:{process:true}});
            });
        };
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
