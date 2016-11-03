angular.module('app.user.edit_user.process',[/*REPLACEMECHILD*/]);
angular.module('app.user.edit_user.process').controller(
    'app.user.edit_user.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.user_id=$state.params.user_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){            
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }        
        $scope.user_info=$state.params.user_info;
        Modals.loading();
        update_user_promise = TimeoutResources.UpdateUser(undefined,{site:$scope.site},$scope.user_info);        
        update_user_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            console.log($scope.resources.updated_user.data);
            Modals.loaded();
        });
    }]
);
