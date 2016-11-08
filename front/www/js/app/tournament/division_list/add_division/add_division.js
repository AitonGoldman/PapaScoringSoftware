angular.module('app.tournament.division_list.add_division',['app.tournament.division_list.add_division.process',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament.division_list.add_division').controller(
    'app.tournament.division_list.add_division',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.tournament_id=$state.params.tournament_id;
        $scope.division = {use_stripe:true,scoring_type:'HERB',tournament_id:$scope.tournament_id};        

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
