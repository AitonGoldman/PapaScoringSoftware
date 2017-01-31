angular.module('app.prereg_complete.confirm.process',[/*REPLACEMECHILD*/]);
angular.module('app.prereg_complete.confirm.process').controller(
    'app.prereg_complete.confirm.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.player_name=$state.params.player_name;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
     
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        player_edit_promise = TimeoutResources.UpdatePlayer($scope.bootstrap_promise,{site:$scope.site,player_id:$scope.player_id},{active:true});
        player_edit_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
    }]
);
