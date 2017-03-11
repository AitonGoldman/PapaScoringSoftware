angular.module('app.prereg_complete',['app.prereg_complete.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.prereg_complete').controller(
    'app.prereg_complete',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        if($state.current.name == 'app.prereg_complete'){
            prereg_players_promise = TimeoutResources.GetPlayersPreregFast($scope.bootstrap_promise,{site:$scope.site});            
        } else {
            prereg_players_promise = TimeoutResources.GetPlayersInLineFast($scope.bootstrap_promise,{site:$scope.site});
        }        
        prereg_players_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.flat_players = _.values($scope.resources.players.data);
            Modals.loaded();
        });
    }]
);
