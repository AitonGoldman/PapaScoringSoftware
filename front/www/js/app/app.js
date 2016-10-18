app = angular.module(
	'TDApp',
    [
        'ionic',
 	'ui.router',            
        'ngCookies',            
        'ngSanitize',
        'app.login',
        'TD_services',
        /*REPLACEMECHILD*/
	]
);

app.controller(
    'IndexController',    
    function($scope, $location, $http, 
             $state,Modals) {
        //Modals.loading();
        //Modals.set_status_modal_message('hi there this is a long message but Im sure you can handle it');
        $scope.site = $state.params.site;
        //Modals.error('Hi There',$scope.site,'app.login');

        //$scope.site = $state.params.site;
        //console.log('in index');
        
        //Utils.controller_bootstrap($scope,$state);
        //$scope.User = User;
    }
);
app.controller(
    'TestController',    
    function($scope, $location, $http, 
             $state, $ionicHistory) {
        $scope.site = $state.params.site;
        console.log('in test 1');
//        console.log($ionicHistory.viewHistory());
        //Utils.controller_bootstrap($scope,$state);
        //$scope.User = User;
    }
);

app.controller(
    'TestController2',    
    function($scope, $location, $http, 
             $state, $ionicHistory) {
        $scope.site = $state.params.site;
        console.log('in tests 2');
        console.log($ionicHistory.viewHistory());
        //Utils.controller_bootstrap($scope,$state);
        //$scope.User = User;
    }
);




