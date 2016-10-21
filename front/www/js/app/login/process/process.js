angular.module('app.login.process',[/*REPLACEMECHILD*/]);
angular.module('app.login.process').controller(
    'app.login.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {            
            $scope.site=$state.params.site;        
            $scope.utils = Utils;
            $scope.controller_bootstrap($scope,$state,true);                
            $scope.process_step=$state.params.process_step;
            $scope.User=User;
            
        if(_.size($scope.process_step)==0){
          Utils.stop_post_reload();
        }
            $scope.user_info=$state.params.user_info;
            
            Modals.loading();            
            $login_promise = TimeoutResources.Login(undefined,{site:$scope.site},
                                                    {username:$scope.user_info.username,password:$scope.user_info.password});
            
        $login_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            User.set_logged_in_user($scope.resources.logged_in_user.data);
            Modals.loaded();
        },function(data){
            //FIXME : need a better way to handle situation where we want
            //        a different error message than what is given back
            //        by the server.            
            //console.log(data.config.url.split('/')[3]);
            Modals.error('Login Failed. Check your username and password.', $scope.site, '^');
        });                     
    }]
);
