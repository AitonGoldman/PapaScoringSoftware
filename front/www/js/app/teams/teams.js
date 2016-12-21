angular.module('app.teams',['app.teams.add_team',
    /*REPLACEMECHILD*/]);
angular.module('app.teams').controller(
    'app.teams',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        teams_promise = TimeoutResources.GetTeams(undefined,{site:$scope.site});
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        teams_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.flat_teams = _.values($scope.resources.teams.data);
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
