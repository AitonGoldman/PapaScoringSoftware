angular.module('app.set_player_picture.take_picture.process',[/*REPLACEMECHILD*/]);
angular.module('app.set_player_picture.take_picture.process').controller(
    'app.set_player_picture.take_picture.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.pic_file=$state.params.pic_file;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        console.log($scope.pic_file);
        $scope.player_info={player_id:$scope.player_id,pic_file:$scope.pic_file};
        update_player_promise = TimeoutResources.UpdatePlayer($scope.bootstrap_promise,{site:$scope.site,player_id:$scope.player_id},$scope.player_info);
        
        // = TimeoutResources.GetEtcData();
        update_player_promise.then(function(data){
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
