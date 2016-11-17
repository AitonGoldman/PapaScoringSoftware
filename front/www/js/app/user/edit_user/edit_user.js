angular.module('app.user.edit_user',['app.user.edit_user.process',
                                     /*REPLACEMECHILD*/]);
angular.module('app.user.edit_user').controller(
    'app.user.edit_user',[
        '$scope','$state','TimeoutResources','Utils','Modals', 'Camera', '$cordovaCamera', '$cordovaFileTransfer',
        function($scope, $state, TimeoutResources, Utils,Modals, Camera, $cordovaCamera, $cordovaFileTransfer) {                        
            $scope.site=$state.params.site;
	    $scope.user_id=$state.params.user_id;

            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            $scope.random_img=_.random(0,99999);
            Modals.loading();
            get_roles_promise = TimeoutResources.GetRoles(undefined,{site:$scope.site});
            get_user_promise = TimeoutResources.GetUser(get_roles_promise,{site:$scope.site,user_id:$scope.user_id});
            
            // = TimeoutResources.GetEtcData();
            get_user_promise.then(function(data){                            
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.user_info = $scope.resources.user.data[$scope.user_id];                                        
                $scope.user_info.roles_dict = {};                
                // for(role_idx in $scope.resources.roles.data){                
                //     role = $scope.resources.roles.data[role_idx];                                                
                //     if(_.findIndex($scope.user_info.existing_roles, function(o) { return o.name == role.name; })!= -1){
                //         $scope.user_info.roles[role.role_id]=true;                    
                //     }
                // }
                _.forEach($scope.resources.roles.data,function(value){
                    if(_.findIndex($scope.user_info.roles, function(o) { return o.name == value.name; })!= -1){
                        $scope.user_info.roles_dict[value.role_id]=true;                    
                    }                    
                });
                Modals.loaded();
            });
        }]
);
