angular.module('app.player_token.confirm.process',[/*REPLACEMECHILD*/]);
angular.module('app.player_token.confirm.process').controller(
    'app.player_token.confirm.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
            $scope.token_info=$state.params.token_info;
            Modals.loading();
            complete_token_promise = TimeoutResources.CompletePlayerTokens(undefined,{site:$scope.site},$scope.token_info);
            
            // = TimeoutResources.GetEtcData();
                complete_token_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    Modals.loaded();
                });
    }]
);
