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
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.user_info=$state.params.user_info;        
        Modals.loading();
        $scope.user_info.roles=[];
        _.forEach($scope.user_info.roles_dict,function(value,key){
            console.log(key+" "+value);
            if(value==true){
                $scope.user_info.roles.push(key);
            }            
        });
        add_user_promise = TimeoutResources.AddUser(undefined,{site:$scope.site},$scope.user_info);
        // = TimeoutResources.GetEtcData();
        add_user_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
