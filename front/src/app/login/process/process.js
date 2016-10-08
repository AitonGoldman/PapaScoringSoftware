angular.module('app.login.process',[/*REPLACEMECHILD*/]);
angular.module('app.login.process').controller(
    'app.login.process',
    function($scope, $state, TimeoutResources) {
        $scope.site=$state.params.site;

	//$scope.player_info=$state.params.newPlayerInfo;
	//if($scope.checkForBlankParams($scope.player_info) == true){
	//    return;
	//}        
    }
);
