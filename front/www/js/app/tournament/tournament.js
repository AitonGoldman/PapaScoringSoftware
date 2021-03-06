angular.module('app.tournament',['app.tournament.add_tournament',
    'app.tournament.edit_tournament',
    'app.tournament.division_list',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament').controller(
    'app.tournament',[
        '$scope','$state','TimeoutResources','Utils','Modals','$timeout','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals, $timeout, ActionSheets) {
            $scope.site=$state.params.site;
            
            $scope.choose_action = ActionSheets.choose_action;
            
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            Modals.loading();
            tournaments_promise = TimeoutResources.GetTournaments($scope.bootstrap_promise,{site:$scope.site});        
            //= TimeoutResources.GetEtcData();
            tournaments_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
            });
            
        }]
);
