angular.module('app.login.process',[/*REPLACEMECHILD*/]);
angular.module('app.login.process').controller(
    'app.login.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','User','$ionicPush','$ionicPlatform',
        function($scope, $state, TimeoutResources, Utils,Modals,User,$ionicPush,$ionicPlatform) {            
            $scope.site=$state.params.site;        
            $scope.utils = Utils;
            //$scope.controller_bootstrap($scope,$state,true);                
            $scope.process_step=$state.params.process_step;
            $scope.User=User;

            if(_.size($scope.process_step)==0){
                //Utils.stop_post_reload();
                //Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
                //return;
                //FIXME : eh, I guess it's okay if you resubmit a login?
            }            
            
            $scope.user_info=$state.params.user_info;
            
            Modals.loading();
            post_obj = {username:$scope.user_info.username,password:$scope.user_info.password};
            if(ionic.Platform.isWebView() == true && ionic.Platform.device().isVirtual==false && ionic.Platform.isIOS() == false){
                ionic_push_promise = $ionicPush.register().then(function(t) {
                    $scope.ioniccloud_push_token = t;
                    post_obj["ioniccloud_push_token"] = $scope.ioniccloud_push_token.token;
                });
            } else {
                ionic_push_promise = Utils.resolved_promise();
            }                                            
            
            $login_promise = TimeoutResources.Login(ionic_push_promise,{site:$scope.site},post_obj);
            
            $login_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                User.set_logged_in_user($scope.resources.logged_in_user.data,"user");
                Modals.loaded();
            },function(data){
                //FIXME : need a better way to handle situation where we want
                //        a different error message than what is given back
                //        by the server.            
                //console.log(data.config.url.split('/')[3]);                
                Modals.error('Login Failed. Check your username and password.', $scope.site, '^');
            });                     
        }
    ]
);
