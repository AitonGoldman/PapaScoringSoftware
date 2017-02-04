angular.module('prereg.step1.step2.step3.step4.confirm',['prereg.step1.step2.step3.step4.confirm.step5',
/*REPLACEMECHILD*/]);
angular.module('prereg.step1.step2.step3.step4.confirm').controller(
    'prereg.step1.step2.step3.step4.confirm',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.linked_division_id=$state.params.linked_division_id;
	$scope.linked_division_name=$state.params.linked_division_name;
	$scope.uploaded_file_name=$state.params.uploaded_file_name;
        $scope.first_name = $state.params.player_first_name;
        $scope.last_name = $state.params.player_last_name;
        $scope.player_email = $state.params.player_email;        
        $scope.ifpa_ranking = $state.params.ifpa_ranking;        
        $scope.uploaded_file_name = $state.params.uploaded_file_name;        
        $scope.player_shirt_size = $state.params.player_shirt_size;        
        $scope.isWebView = ionic.Platform.isWebView();        

        $scope.utils = Utils;

        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
