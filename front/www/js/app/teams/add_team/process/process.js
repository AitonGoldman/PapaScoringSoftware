angular.module('app.teams.add_team.process',[/*REPLACEMECHILD*/]);
angular.module('app.teams.add_team.process').controller(
    'app.teams.add_team.process',[
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
        
        $scope.team_info=$state.params.team_info;
        add_team_promise = TimeoutResources.AddTeam($scope.bootstrap_promise,{site:$scope.site},$scope.team_info);
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        add_team_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
    }]
);
