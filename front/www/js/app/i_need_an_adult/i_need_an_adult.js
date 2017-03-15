angular.module('app.i_need_an_adult',['app.i_need_an_adult.process',
    /*REPLACEMECHILD*/]);
angular.module('app.i_need_an_adult').controller(
    'app.i_need_an_adult',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
        $scope.page_info = {division:undefined};
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                            
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        $scope.bootstrap_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.tournaments = _.filter($scope.resources.divisions.data, function(o) { return o.division_id; });
            Modals.loaded();
        });
    }]
);
