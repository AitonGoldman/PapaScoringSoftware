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
                url="http://0.0.0.0:8000/"+$state.params.event_name+"/media_upload/jpg_pic";
                header_links[0]['link'] = '.manage_tournaments.edit_tournament_advanced({id:'+$state.params.id+'})';
            }
            if(edit_route=="put_edit_event"){
                url = "http://0.0.0.0:8000/pss_admin/media_upload/jpg_pic";
                header_links[0]['link'] = '.pss_admin.edit_event_advanced({id:'+$state.params.id+'})';
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

            
            if($scope.wizard_step == undefined){                
                basic_or_advanced_edit=true;
            }
            if(_.isEmpty($state.params.item) && $scope.wizard_step > 1){
                $state.go('^');
            }
            if($scope.wizard_step>1){                
                $scope.item=$state.params.item;
                $scope.descriptions=$state.params.descriptions;
            }
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
            
            if(basic_or_advanced_edit == true || $scope.wizard_step == 1) {
                var prom =resourceWrapperService.get_wrapper_with_loading(get_route,on_get_success,{event_name:$state.params.event_name,id:$state.params.id},{});                
            }                                    
                                    
            $scope.edit_event_func = function(old_event,result_fields){                
                old_event.wizard_configured=true;
                var prom =resourceWrapperService.get_wrapper_with_loading(edit_route,on_edit_success,{id:$state.params.id,event_name:$state.params.event_name},old_event);
            };
            
        }
    ]);
