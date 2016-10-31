angular.module('app.user.add_user.process',[/*REPLACEMECHILD*/]);
angular.module('app.user.add_user.process').controller(
    'app.user.add_user.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
          Utils.stop_post_reload();
        }
        
        $scope.user_info=$state.params.user_info;
        console.log('hi there');
        console.log($scope.user_info);
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResource.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
