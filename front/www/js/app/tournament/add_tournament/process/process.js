angular.module('app.tournament.add_tournament.process',[/*REPLACEMECHILD*/]);
angular.module('app.tournament.add_tournament.process').controller(
    'app.tournament.add_tournament.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        $scope.tournament_info=$state.params.tournament_info;        
        Modals.loading();
        add_tournament_promise = TimeoutResources.AddTournament(undefined,{site:$scope.site},$scope.tournament_info);        
        // = TimeoutResources.GetEtcData();
        add_tournament_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });        
    }]
);
