angular.module('app.token.token_select.confirm.process',[/*REPLACEMECHILD*/]);
angular.module('app.token.token_select.confirm.process').controller(
    'app.token.token_select.confirm.process',[
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
        
        $scope.token_info=$state.params.token_info;
        divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});
        token_add_promise = TimeoutResources.AddTokens(divisions_promise,{site:$scope.site},$scope.token_info);                
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        //$scope.token_summary = {divisions:{},metadivisions:{}};
        token_add_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
