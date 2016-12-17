angular.module('app.login_player.process',[/*REPLACEMECHILD*/]);
angular.module('app.login_player.process').controller(
    'app.login_player.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.player=$state.params.player;
        Modals.loading();            
        login_promise = TimeoutResources.LoginPlayer(undefined,{site:$scope.site},
                                                {player_pin:$scope.player.pin});
        
        login_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            User.set_logged_in_user($scope.resources.logged_in_player.data,"player");            
            Modals.loaded();
        },function(data){
            //FIXME : need a better way to handle situation where we want
            //        a different error message than what is given back
            //        by the server.            
            //console.log(data.config.url.split('/')[3]);
            Modals.error('Login Failed. Check your pin #.', $scope.site, '^');
        });                     
     
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
