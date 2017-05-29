angular.module('app.token.token_select.confirm.process',[/*REPLACEMECHILD*/]);
angular.module('app.token.token_select.confirm.process').controller(
    'app.token.token_select.confirm.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicHistory) {
            $scope.state=$state.current.name;
            $scope.site=$state.params.site;
	    $scope.player_id=$state.params.player_id;
            $ionicHistory.nextViewOptions({disableBack:true});            
            if($state.current.name=='app.token_comp.token_select_comp.confirm.process'){
                $scope.comp_or_purchase_title="Tickets Comped";                
            } else {
                $scope.comp_or_purchase_title="Tickets Purchased";
            }

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
            
        $scope.token_info=$state.params.token_info;
        $scope.total_cost=$state.params.total_cost;
        divisions_promise = TimeoutResources.GetDivisions($scope.bootstrap_promise,{site:$scope.site});
        token_add_promise = TimeoutResources.AddTokens(divisions_promise,{site:$scope.site},$scope.token_info);
        
        // = TimeoutResources.GetEtcData();
        //$scope.token_summary = {divisions:{},metadivisions:{}};
        token_add_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            console.log($scope.resources);            
            Modals.loaded();
        });
    }]
);
