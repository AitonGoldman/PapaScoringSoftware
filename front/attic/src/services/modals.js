angular.module('TD_services.modals', ['ngMaterial']);
angular.module('TD_services.modals').factory('Modals', ['$state','$mdDialog','$timeout',function($state,$mdDialog,$timeout) {
    status_message="loading...";    
    status_modal_handle=undefined;
        
    return {
        //FIXME : this should not be here - we should pass site in when needed
        loaded: function(){                        
            $timeout(function(){
                $mdDialog.cancel();
                status_modal_handle = undefined;
            },500);            
        },
        close_latest: function(){
            $mdDialog.cancel(status_modal_handle);
        },
        error:function(error_message,dest_site,dest_route){
            var parentEl = angular.element(document.body);            
            cancel_promise = $mdDialog.cancel();
            cancel_promise.then(function(data){
                status_modal_handle = $mdDialog.show({
                    parent: parentEl,                
                    templateUrl:"services/error_modal.html",
                    //locals: {
                    //     message: status_message
                    //},
                    controller: ['$scope','$mdDialog',function($scope,$mdDialog){
                        $scope.message = error_message;
                        $scope.closeDialog = function() {
                            $mdDialog.cancel();
                            status_modal_handle = undefined;
                            if(dest_route == undefined){
                                dest_route='app';
                            }
                            $state.go(dest_route,{site:dest_site});
                        };
                    }]                
                });
            });            
        },
        loading: function(){
            var parentEl = angular.element(document.body);
            if(status_modal_handle == undefined){
                status_modal_handle = $mdDialog.show({
                    parent: parentEl,                
                    templateUrl:"services/status_modal.html",
                    //locals: {
                    //     message: status_message
                    //},
                    controller: ['$scope','$mdDialog',function($scope,$mdDialog){
                        $scope.message = status_message;
                    }]
                    
                });
            }
        },
        set_status_modal_message: function(message){
            status_message=message;
        }
    };
}]);

