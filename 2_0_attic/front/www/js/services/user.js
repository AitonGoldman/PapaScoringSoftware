angular.module('TD_services.user', []);
angular.module('TD_services.user').factory('User', ['Modals','TimeoutResources','$state',function(Modals,TimeoutResources,$state) {

    var logged_in_user = undefined;
    var logged_in_player = undefined;
    var logged_in_status = false;
    var type_of_user = undefined;
    var user_site = undefined;
    var login_time = undefined;
    var set_logged_in_user_func = function(new_user,new_user_type) {        
        logged_in_user = new_user;
        type_of_user = new_user_type;
        logged_in_status=true;
        login_time = new Date();
    };

    
    return {
        log_out: function(){
            logged_in_status=false;
            logged_in_user=undefined;
        },
        set_user_site: function(new_site){
            user_site = new_site;
        },
        get_user_site: function(){
            return user_site;
        },        
        check_current_user:function(){
            
            //Modals.loading();            
            $current_user_promise = TimeoutResources.CurrentUser(undefined,{site:user_site});
            return $current_user_promise.then(function(data){                                
                if(data.data!=null){
                    console.log(data);
                    if(data.data.player_id!=undefined){
                        set_logged_in_user_func(data.data,'player');
                    } else {
                        set_logged_in_user_func(data.data,'user');
                    }
                }
                //Modals.loaded();
            },function(data){
                //FIXME : If you are not logged in, you will be whisked away to login page
                //        this can be confusing, and needs to pop up a "hey - you are not
                //        logged in - click ok to login" message
                $state.go('app.login',{site:user_site});
                //Modals.loaded();
            });            
        },
        logged_in: function(){
            return logged_in_status;  
        },
        logged_in_user: function() {            
//            if(type_of_user == "user"){
                return logged_in_user;
  //          }
    //        if(type_of_user == "player"){
    //            return logged_in_player;
   //         }
            //return undefined;
        },        
        set_logged_in_user:  set_logged_in_user_func,         
        has_role: function(role) { 
            return logged_in_user && logged_in_user.roles && (
                //logged_in_user.roles.indexOf(role) != -1
                _.find(logged_in_user.roles, function(o) { return o.name == role; })
            )? true: false;
        }
    };
}]);


