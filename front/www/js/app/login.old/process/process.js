angular.module('app.login.process', []);
angular.module('app.login.process')
    .controller('app.login.process', function($scope, $ionicModal, $timeout, $state,User) {
        $scope.user = $state.params.user_info;
        console.log('in process');
        console.log($scope.user);
});
