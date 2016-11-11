app = angular.module(
	'TDApp',
    [
        'ionic',
        'ngCordova',
 	'ui.router',            
        'ngCookies',            
        'ngSanitize',
        'app.login',
        'TD_services',
        'app.login',
    'app.logout',
    'app.user',
    'app.tournament',
    /*REPLACEMECHILD*/
	]
);

app.controller(
    'IndexController',    
    function($scope, $location, $http, 
             $state,Modals, User, Utils,$ionicPlatform, $ionicActionSheet, TimeoutResources) {
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
            $scope.menu_bar_title_style={'height':'120'};
        }
        $scope.is_native = false;
        $ionicPlatform.ready(function() {        
            dev_info = ionic.Platform.device();
            if (_.size(dev_info)!=0){
                $scope.is_native=true;
                //alert('on a native app');
            }
        });
        $scope.choose_action = function(division_id,tournament,dest_route){
            
            var hideSheet = $ionicActionSheet.show({
                buttons: [
                    { text: 'Edit Tournament' },
                    { text: 'Activate/Deactivate Tournament' }
                ],                    
                titleText: 'Tournament Actions',
                cancelText: 'Cancel',
                cancel: function() {
                    // add cancel code..
                },
                buttonClicked: function(index) {
                    if(index == 0){
                        $state.go(dest_route,{division_id:division_id});
                    }
                    if(index == 1){
                        if(tournament.active == true){
                            new_tournament_status=false;
                            tournament.active=false;
                        } else {                                
                            new_tournament_status=true;
                            tournament.active=true;
                        }
                        Modals.loading();
                        active_promise = TimeoutResources.UpdateDivision(undefined,{site:$scope.site},{division_id:division_id,active:new_tournament_status});
                        active_promise.then(function(data){
                            Modals.loaded();
                        });
                    }
                    return true;
                }
            });
        };          
    }
);

app.run(function($ionicPlatform) {
  });
  

app.config(function($httpProvider,$ionicConfigProvider) {
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.withCredentials = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
    $ionicConfigProvider.backButton.previousTitleText(false);
    $ionicConfigProvider.backButton.icon('ion-arrow-left-a');
});

app.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i=0; i<total; i++) {
      input.push(i);
    }

    return input;
  };
});

