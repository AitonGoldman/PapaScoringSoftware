angular.module('shared',[]);
angular.module('shared').controller(
    'app.shared.edit_event_tournament_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope','eventTournamentLib','$http','FileUploader','$ionicScrollDelegate',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope,eventTournamentLib,$http,FileUploader,$ionicScrollDelegate ) {                        
            $scope.bootstrap({back_button:true});
            var header_links=[{icon:'ion-edit',label:'Advanced Edit'}];            
            $scope.wizard_step = $state.params.wizard_step;                                    
            var edit_route = $state.current.data.edit_route;
            var get_route = $state.current.data.get_route;                        
            var basic_or_advanced_edit=false;
            var file_form_data = {type:edit_route,id:$state.params.id};            
            $scope.uploaded_file=false;

            var url = "";
            if(edit_route=="put_edit_tournament"){
                url="http://"+backend_ip+":"+backend_port+"/"+$state.params.event_name+"/media_upload/jpg_pic";
                header_links[0]['link'] = '.manage_tournaments.edit_tournament_advanced({id:'+$state.params.id+'})';
            }
            if(edit_route=="put_edit_event"){
                url = "http://"+backend_ip+":"+backend_port+"/pss_admin/media_upload/jpg_pic";
                header_links[0]['link'] = '.edit_event_advanced({id:'+$state.params.id+'})';
            }            
            $scope.add_header_links(header_links);
            $scope.uploader = new FileUploader({url:url,formData:[file_form_data]});            
            $scope.uploader.onSuccessItem=function(item, response, status, headers){
                $scope.item.img_url=response.data;                
                $scope.pic_selected=false;                
                $scope.item.has_pic=true;
            };
            $scope.uploader.onAfterAddingFile = function(fileItem) {                
                $scope.pic_selected=true;
            };            

            
            //if($scope.wizard_step == undefined){                
            //    basic_or_advanced_edit=true;
            //}
            // if(_.isEmpty($state.params.item) && $scope.wizard_step > 1){
            //     $state.go('^');
            // }
            // if($scope.wizard_step>1){                
            //     $scope.item=$state.params.item;
            //     $scope.descriptions=$state.params.descriptions;
            // }
            var on_get_success = function(data){                    
                $scope.item=data['item'];
                var orig_item_fields=[];
                for(i in $scope.item){
                    orig_item_fields.push(i);
                }
                $scope.item.bobo={};
                for(idx in orig_item_fields){
                    field_name = orig_item_fields[idx];
                    $scope.item.bobo[field_name]=$scope.item[field_name];
                }
                $scope.descriptions=data['descriptions'];
                if($scope.item.has_pic==true){
                    $scope.event_image_url='/img/events/'+$state.params.id+'/'+$state.params.id+'.jpg';
                }                
            };

            var on_edit_success = function(data){                    
                var results = [];
                credentialsService.increment_wizard_stack_index($scope.event_name,'event_create');
                var item = data['item'];                    
                for(field_name in item){
                    if(field_name=="bobo"){continue;}
                    if(field_name=="wizard_configured"){continue;}
                    if(field_name=="has_pic"){continue;}                    
                    if(_.isArray(item[field_name])){continue;}
                    if(_.isObject(item[field_name])){continue;}                                            
                    if(field_name=="img_url"){
                        results.push(['New Image Uploaded','True']);
                        continue;
                    }                                        
                    if($scope.item.bobo[field_name]!=item[field_name]){
                        results.push([$scope.descriptions.short_descriptions[field_name],item[field_name]]);   
                    };                    
                }                
                $scope.post_success_handler("Event Edited!",results,$scope);
                //FIXME : results page needs to say something about "these are the changed fields" on edit
            };                                
            
            //if(basic_or_advanced_edit == true || $scope.wizard_step == 1) {
                var prom =resourceWrapperService.get_wrapper_with_loading(get_route,on_get_success,{event_name:$state.params.event_name,id:$state.params.id},{});                
            //}                                    
                                    
            $scope.edit_event_func = function(old_event,result_fields){                
                //old_event.wizard_configured=true;
                var prom =resourceWrapperService.get_wrapper_with_loading(edit_route,on_edit_success,{id:$state.params.id,event_name:$state.params.event_name},old_event);
            };
            
        }
    ]);

angular.module('shared').controller(
    'app.shared.quick_create_user',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope','eventTournamentLib','$http','FileUploader','$ionicScrollDelegate','$ionicPopup',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope,eventTournamentLib,$http,FileUploader,$ionicScrollDelegate,$ionicPopup ) {                        
            $scope.bootstrap({back_button:true});            
            $scope.filter_for={};
            $scope.new_users={};
            $scope.signal_added_user=false;
            $scope.event_id=$state.params.event_id;
            $scope.event_name=$scope.event_name;
            $scope.target_event_name=$state.params.target_event_name;
            $scope.add_new_player_to_list = function(new_player_name){                
                $scope.signal_added_user= $scope.signal_added_user==false;
                
                var full_name = new_player_name.split(" ");
                console.log(full_name);                
                $scope.filter_for.filter_for="";
                $scope.items.push({
                    first_name:full_name[0],
                    last_name:full_name[1],
                    full_user_name:full_name[0]+" "+full_name[1],
                    checked:true,
                    username: full_name[0]+full_name[1],
                    already_checked:false
                });
            };
            // ionic.DomUtil.ready(function(){
            //     $ionicScrollDelegate.$getByHandle('tournamentlist').getScrollPosition().left;
            //     var myElement = angular.element( document.querySelector( '.pooping' ) );
            //     console.log('poop');
            //     $scope.scrollAmount = myElement[0].clientWidth;                
            // });
            $scope.scroll_left = function(){
                $ionicScrollDelegate.$getByHandle('tournamentlist').scrollBy($scope.scrollAmount-($scope.scrollAmount/4),undefined,true);
            };
            $scope.showConfirm = function(user_type) {
                var confirmPopup = $ionicPopup.alert({
                    title: 'Users to register as '+user_type+'s',
                    templateUrl: 'templates/registered_users_list.html',
                    scope:$scope
                });
            };            

            $scope.event_role_name=$state.params.event_role_name;
            var header_links=[{icon:'ion-edit',label:'Advanced Edit'}];            
            var mark_users_in_event = function(u){
                var user_is_in_event = _.filter(u.events,function(e){
                    var u_in_event = e.event_id==$scope.event_id;
                    var role_in_event = _.filter(u.event_roles,function(r){
                        return r.event_role_id==$scope.event_role_id;                        
                    }).length>0;
                    return u_in_event==true && role_in_event==true;
                }).length>0;
                
                if(user_is_in_event==true){
                    u.already_checked=true;
                    u.checked=true;
                }else{
                    u.already_checked=false;
                }
            };
            var on_get_success = function(data){                    
                $scope.event_roles = data['event_roles'];
                //var event_role_name=$state.params.event_role_name;
                if($scope.event_role_name=='scorekeeper'){
                    $scope.type_of_user=$scope.event_role_name;
                }
                if($scope.event_role_name=='deskworker'){
                    $scope.type_of_user="desk worker";
                }
                if($scope.event_role_name=='tournament_director'){
                    $scope.type_of_user='tournament director';
                }
                
                $scope.event_role_id = _.filter($scope.event_roles, function(o) { return o.name==$scope.event_role_name; })[0].event_role_id;
                $scope.new_users.event_id=$state.params.event_id;
                $scope.new_users.event_role_id=$scope.event_role_id;

                var items = data['existing_pss_users'];
                var pss_user_id = credentialsService.get_credentials()[$scope.event_name].pss_user_id;
                $scope.items = _.filter(items, function(o) { return o.pss_user_id!=pss_user_id; });
                //$scope.bobo_items = _.filter(items, function(o) { return o.checked==true; });
                _.map(items, mark_users_in_event);
                //$scope.checked_items = _.filter(items, function(o) { return o.checked==true; });
                console.log($scope.items);
            };
            var on_post_success = function(data){                    
                $scope.new_items = data['pss_users_added_to_event'];
                var results = _.map($scope.new_items, function(o){return ['User Registered',o.full_user_name];});                      
                $scope.post_success_handler("Users Registered!",results,$scope,{title:'Attention',text:'Remember!  You will need to set user passwords once they arrive at the event.'});
                console.log($scope.new_items);                
            };            
            
            $scope.add_text_area_users_func = function(){                
                var bulk_add_prom =resourceWrapperService.get_wrapper_with_loading("post_add_event_users",on_post_success,{event_name:$scope.event_name},$scope.new_users);
            };
            $scope.add_existing_users_func = function(){                                
                var users = _.filter($scope.items, function(o) { return o.checked==true; });
                console.log(users);
                var submit_json = {event_id:$scope.event_id,event_role_id:$scope.event_role_id,users:users};
                
                var bulk_add_prom =resourceWrapperService.get_wrapper_with_loading("put_add_existing_users",on_post_success,{event_name:$scope.event_name},submit_json);
            };
            
            var prom =resourceWrapperService.get_wrapper_with_loading("get_users",on_get_success,{event_name:$scope.target_event_name},{});
            
        }
    ]);
