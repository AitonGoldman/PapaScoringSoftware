angular.module('TD_services.camera',[]);
angular.module('TD_services.camera').factory('Camera', ['$state','$timeout','$rootScope','Modals', '$cordovaCamera', '$cordovaFileTransfer', function($state,$timeout,$rootScope, Modals, $cordovaCamera, $cordovaFileTransfer) {            
    var dest_pic_name="1.jpg";
    //var upload_host=http_prefix+"://98.111.232.93:8000";
    var upload_host=http_prefix+"://"+server_ip_address+":8000";    
    var upload_url_path="/test/media_upload/user_pic";
    var TRANSFER_FAILED='transfer failed';
    var TRANSFER_SUCCESS='transfer success';
    var CAMERA_FAILED='camera failed';
    var upload_url=function(){
        return upload_host+upload_url_path;
    };
    
    return{
        take_user_pic_and_upload: function(type_of_pic,site,id){
            //FIXME : need to use ngCordova so we can have proper callbacks, and thus unset has_picture if needed                                                                
            take_pic_promise = $cordovaCamera.getPicture({targetWidth:200,targetHeight:200}).then(function(imageUri) {                
                return imageUri;
            }, function(err) {
                
            });            
            return take_pic_promise.then(function(data){                                    
                //var image = document.getElementById('user_edit_user_pic');                                       
                //image.src=data;
                if(data == undefined){
                    return;
                }
                Modals.loading();
                var localFileName = data.substr(data.lastIndexOf('/') + 1);
                var randomNumber = Math.floor((Math.random() * 1000) + 1); 
                if(id == undefined){
                    var dest_pic_name=localFileName+"-"+randomNumber+".jpg";
                } else {
                    var dest_pic_name="player_"+id+".jpg";
                }
                
                //var dest_pic_name=user_id+".jpg";
                //var upload_host="http://98.111.232.93:8000";
                //var upload_host="http://192.168.1.178:8000";
                var upload_host=http_prefix+"://"+server_ip_address+":"+server_port;
                var upload_url_path="/"+site+"/media_upload/"+type_of_pic+"_pic";            
                var cordova_options = {};
                cordova_options.timeout = 10000;
                cordova_options.chunkedMode = false;
                cordova_options.fileKey = "file";        
                cordova_options.fileName = dest_pic_name;                
                return $cordovaFileTransfer.upload(upload_host+upload_url_path, data, cordova_options, true)
                    .then(function(result) {
                        Modals.loaded();                        
                        return {result:TRANSFER_SUCCESS,file_name:JSON.parse(result.response).data,local_file_path:data};
                    }, function(err) {
                        Modals.loaded();
                        alert('transfer is bad '+err.code);                        
                        return {result:TRANSFER_FAILED};
                    });                                        
            }, function(err){
                Modals.loaded();
                alert('aborted camera');
                return {result:CAMERA_FAILED};
            });            
        },
        TRANSFER_FAILED:TRANSFER_FAILED,
        TRANSFER_SUCCESS:TRANSFER_SUCCESS,
        CAMERA_FAILED:CAMERA_FAILED
    };    
}]);
