angular.module('app.oops',['app.oops.edit_player_entries',
    'app.oops.missing_tokens',
    'app.oops.missing_scores',
    /*REPLACEMECHILD*/]);
angular.module('app.oops').controller(
    'app.oops',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

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
