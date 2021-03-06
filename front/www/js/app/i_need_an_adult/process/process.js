angular.module('app.i_need_an_adult.process',[/*REPLACEMECHILD*/]);
angular.module('app.i_need_an_adult.process').controller(
    'app.i_need_an_adult.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
        $scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        if($scope.division_id==-1){
            adult_promise = TimeoutResources.INeedAnAdultAtDesk(undefined,{site:$scope.site});
        } else {
            adult_promise = TimeoutResources.INeedAnAdult(undefined,{site:$scope.site,division_id:$scope.division_id});
        }
        
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        adult_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
