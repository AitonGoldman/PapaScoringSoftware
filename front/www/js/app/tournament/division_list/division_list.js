angular.module('app.tournament.division_list',['app.tournament.division_list.add_division',
    'app.tournament.division_list.edit_division',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament.division_list').controller(
    'app.tournament.division_list',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
            $scope.ActionSheets=ActionSheets;
        $scope.site=$state.params.site;
	$scope.tournament_id=$state.params.tournament_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        tournament_divisions_promise = TimeoutResources.GetTournamentDivisions(undefined,{site:$scope.site,tournament_id:$scope.tournament_id});
        
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        tournament_divisions_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
      
    }]
);
