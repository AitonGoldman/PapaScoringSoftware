angular.module('TD_services.modals',[]);
angular.module('TD_services.modals').factory('Modals', ['$state','$timeout','$ionicLoading','$ionicModal','$rootScope',function($state,$timeout,$ionicLoading,$ionicModal,$rootScope) {        
    error_modal = undefined;
    dest_site = undefined;
    dest_route = undefined;
    
    $rootScope.close_error_dialog = function(){
        error_modal.remove();
        $state.go(dest_route,{site:dest_site});
    };
    
    return {
        //FIXME : this should not be here - we should pass site in when needed
        loaded: function(){                        
            $timeout(function(){
                $ionicLoading.hide();                                
            },500);            
        },
        error:function(error_message,new_dest_site,new_dest_route){
            $ionicLoading.hide();
            $rootScope.error_message = error_message;            
            dest_site = new_dest_site;
            dest_route = new_dest_route;
            if(dest_route == undefined){
                dest_route="app";
            }            
            $ionicModal.fromTemplateUrl('js/services/error_modal.html', {                
                animation: 'slide-in-up',
                backdropClickToClose: false,
                scope : $rootScope
            }).then(function(modal) {
                error_modal = modal;
                error_modal.show();
            });
        },
        loading: function(){
            $ionicLoading.show({
                hideOnStateChange: true,
                template: '<div class="col"><div><ion-spinner></ion-spinner></div><div><br>Loading...<br>{{loading_message}}</div></div>'
            });            
        },
        set_status_modal_message: function(message){
            $rootScope.loading_message=message;
        }
    };
}]);

