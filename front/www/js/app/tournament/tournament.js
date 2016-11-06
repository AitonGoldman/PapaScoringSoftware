angular.module('app.tournament',['app.tournament.add_tournament',
    'app.tournament.edit_tournament',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament').controller(
    'app.tournament',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        Modals.loading();
        tournaments_promise = TimeoutResources.GetTournaments(undefined,{site:$scope.site});        
        //= TimeoutResources.GetEtcData();
        tournaments_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
