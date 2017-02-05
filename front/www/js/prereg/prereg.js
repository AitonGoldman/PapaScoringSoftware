angular.module('prereg',['prereg.step1',
    /*REPLACEMECHILD*/]);
angular.module('prereg').controller(
    'prereg',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicScrollDelegate',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicScrollDelegate) {
        $scope.site=$state.params.site;
        window.addEventListener('native.keyboardshow', function(){
            $ionicScrollDelegate.scrollBy(0,200);
        });
        $scope.utils = Utils;
        $scope.isWebView = ionic.Platform.isWebView();        
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
