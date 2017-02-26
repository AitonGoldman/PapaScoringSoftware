angular.module('app.ppo_qualifying_list',['app.ppo_qualifying_list.qualifiers',
    'app.ppo_qualifying_list.papa_qualifiers',
    /*REPLACEMECHILD*/]);
angular.module('app.ppo_qualifying_list').controller(
    'app.ppo_qualifying_list',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.resources = TimeoutResources.GetAllResources();             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
