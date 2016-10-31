app = angular.module(
	'TDApp',
    [
        'ionic',
 	'ui.router',            
        'ngCookies',            
        'ngSanitize',
        'app.login',
        'TD_services',
        'app.login',
    'app.logout',
    'app.user',
    /*REPLACEMECHILD*/
	]
);

app.controller(
    'IndexController',    
    function($scope, $location, $http, 
             $state,Modals, User, Utils,Camera) {
        $scope.Camera=Camera;
        //FIXME : there has got to be a better place to put this, but I can't put it in
        //        Utils because it will cause a circular reference
        $scope.controller_bootstrap = function(scope, state, do_not_check_current_user){
            scope.site=state.params.site;
            User.set_user_site(scope.site);            
            if(do_not_check_current_user == undefined && User.logged_in() == false){
                return User.check_current_user();
            } else {
                return Utils.resolved_promise();
            }                                 
        };
        
        $scope.controller_bootstrap($scope,$state);
        $scope.User = User;
        $scope.isIOS = ionic.Platform.isIOS();
        //FIXME : don't need this anymore
        if($scope.isIOS == true){
            $scope.menu_bar_title_style={'height':'100'};
        } else {
            $scope.menu_bar_title_style={'height':'100'};
        }
    }
);



app.config(function($httpProvider,$ionicConfigProvider) {
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.withCredentials = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
    $ionicConfigProvider.backButton.previousTitleText(false);
    $ionicConfigProvider.backButton.icon('ion-arrow-left-a');
});



