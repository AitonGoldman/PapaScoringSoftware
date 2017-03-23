angular.module('TD_services.modals',[]);
angular.module('TD_services.modals').factory('Modals', ['$state','$timeout','$ionicLoading','$ionicModal','$rootScope',function($state,$timeout,$ionicLoading,$ionicModal,$rootScope) {        
    error_modal = undefined;
    choose_machine_modal = undefined;
    dest_site = undefined;
    dest_route = undefined;

    $rootScope.machines = {1:{machine_id:1,machine_name:'disney tron'},2:{machine_id:2,machine_name:'tron'},3:{machine_id:3,machine_name:'whatever'}};
    $rootScope.matches = [];

    
    $rootScope.close_error_dialog = function(){        
        return error_modal.remove().then(function(data){
            error_modal = undefined;
            $state.go(dest_route,{site:dest_site});
        });            
    };
    
    return {
        //FIXME : this should not be here - we should pass site in when needed
        loaded: function(){            
            $timeout(function(){                
                $ionicLoading.hide();                                
            },500);            
        },
        information:function(message){
            console.log(message);
            if (_.isArray(message)){
                $rootScope.isArray=true;
            } else {
                $rootScope.isArray=false;
            }            
            $ionicModal.fromTemplateUrl('js/services/information_modal.html', {                
                animation: 'slide-in-up',
                backdropClickToClose: false,
                scope : $rootScope
            }).then(function(modal) {
                $rootScope.message = message;                            
                $rootScope.information_modal = modal;
                $rootScope.information_modal.show();
            });            
        },
        error:function(error_message,new_dest_site,new_dest_route){            
            $ionicLoading.hide();                                
            if(error_modal != undefined){
                return;
            }
            error_modal='dummy';
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
        choose_machine:function(){                        
            $ionicLoading.hide();                                
            if(choose_machine_modal != undefined){
                return;
            }
            choose_machine_modal='dummy';
            //$rootScope.error_message = error_message;            
            //dest_site = new_dest_site;
            //dest_route = new_dest_route;
            //if(dest_route == undefined){
            //    dest_route="app";
            //}            
            $ionicModal.fromTemplateUrl('js/services/select_machine.html', {                
                animation: 'slide-in-up',
                backdropClickToClose: false,
                scope : $rootScope
            }).then(function(modal) {
                choose_machine_modal = modal;
                choose_machine_modal.show();
            });
        },        
        loading: function(){
            $ionicLoading.show({
                hideOnStateChange: true,
                template: '<div class="col"><div><ion-spinner></ion-spinner></div><div><br>Loading...<br>{{loading_message}}</div></div>'
            });            
        },
        loading_no_spinner: function(){
            $ionicLoading.show({
                hideOnStateChange: true,
                template: '<div><br>Loading...<br>{{loading_message}}</div>'
            });            
        },        
        set_status_modal_message: function(message){
            $rootScope.loading_message=message;
        }
    };
}]);

