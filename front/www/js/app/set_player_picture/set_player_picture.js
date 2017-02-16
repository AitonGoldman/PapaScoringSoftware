angular.module('app.set_player_picture',['app.set_player_picture.take_picture',
    /*REPLACEMECHILD*/]);
angular.module('app.set_player_picture').controller(
    'app.set_player_picture',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        players_promise = TimeoutResources.GetPlayersFast($scope.bootstrap_promise,{site:$scope.site});
        
        // = TimeoutResources.GetEtcData();
        players_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.flat_players = _.filter(_.values($scope.resources.players.data), function(o) { return !o.has_pic; });
            
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
