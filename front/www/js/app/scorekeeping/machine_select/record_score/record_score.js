angular.module('app.scorekeeping.machine_select.record_score',['app.scorekeeping.machine_select.record_score.void',
    'app.scorekeeping.machine_select.record_score.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.record_score').controller(
    'app.scorekeeping.machine_select.record_score',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
        $scope.division_machine_id=$state.params.division_machine_id;
        $scope.division_machine_name=$state.params.division_machine_name;
            $scope.player_id = $state.params.player_id;
            $scope.player_name = $state.params.player_name;
            $scope.choose_void_action = ActionSheets.choose_void_action;
            
        $scope.score={score:undefined};
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.resources = TimeoutResources.GetAllResources();
        console.log($scope.resources);
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
            //})
            $scope.test_submit = function(){                
                $state.go('.confirm',{score:$scope.score.score});
            };
            
    }]
);