angular.module('app.login',['app.login.process'])
    .controller('app.login', function($scope, $ionicModal, $timeout) {
        $scope.user = {};
        console.log('in logins');
});
