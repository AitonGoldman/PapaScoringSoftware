angular.module('app.login_player.process',[/*REPLACEMECHILD*/]);
angular.module('app.login_player.process').controller(
    'app.login_player.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','User','$ionicPush','$ionicPlatform',
        function($scope, $state, TimeoutResources, Utils,Modals,User, $ionicPush, $ionicPlatform) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
            $scope.player=$state.params.player;
            Modals.loading();            
            post_obj = {player_pin:$scope.player.pin,player_id:$scope.player.player_id};
            if(ionic.Platform.isWebView() == true && ionic.Platform.device().isVirtual==false){                
                ionic_push_promise = $ionicPush.register().then(function(t) {
                    $scope.ioniccloud_push_token = t;
                    post_obj["ioniccloud_push_token"] = $scope.ioniccloud_push_token.token;
                },function(error){
                    alert('Something has gone wrong while logging in.  Please see the front desk');
                });                
            } else {
                ionic_push_promise = Utils.resolved_promise();
            }                                            
            logout_promise = TimeoutResources.Logout(ionic_push_promise,{site:$scope.site});

            login_promise = TimeoutResources.LoginPlayer(logout_promise,{site:$scope.site},post_obj);
        
        login_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            console.log($scope.resources);
            User.set_logged_in_user($scope.resources.logged_in_player.data,"player");            
            Modals.loaded();
        },function(data){            
            //FIXME : need a better way to handle situation where we want
            //        a different error message than what is given back
            //        by the server.            
            //console.log(data.config.url.split('/')[3]);
            Modals.error('Login Failed. Check your player # and pin #.', $scope.site, '^');
        });                     
     
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
