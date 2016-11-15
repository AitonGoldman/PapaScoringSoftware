angular.module('TD_services.camera',[]);
angular.module('TD_services.camera').factory('Camera', ['$state','$timeout','$rootScope','Modals', '$cordovaCamera', '$cordovaFileTransfer', function($state,$timeout,$rootScope, Modals, $cordovaCamera, $cordovaFileTransfer) {            
    var dest_pic_name="1.jpg";
    var upload_host="http://98.111.232.93:8000";
    var upload_url_path="/test/media_upload/user_pic";
    var TRANSFER_FAILED='transfer failed';
    var TRANSFER_SUCCESS='transfer success';
    var CAMERA_FAILED='camera failed';
    var upload_url=function(){
        return upload_host+upload_url_path;
    };
    
    return{
        take_user_pic_and_upload: function(type_of_pic){
            //FIXME : need to use ngCordova so we can have proper callbacks, and thus unset has_picture if needed                                                                
            take_pic_promise = $cordovaCamera.getPicture({}).then(function(imageUri) {
                return imageUri;
            }, function(err) {
                
            });            
            return take_pic_promise.then(function(data){                    
                var image = document.getElementById('user_edit_user_pic');                                       
                image.src=data;

                var localFileName = data.substr(data.lastIndexOf('/') + 1);
                var randomNumber = Math.floor((Math.random() * 1000) + 1); 
                var dest_pic_name=localFileName+"-"+randomNumber+".jpg";
                //var dest_pic_name=user_id+".jpg";
                var upload_host="http://98.111.232.93:8000";
                var upload_url_path="/test/media_upload/"+type_of_pic+"_pic";            
                var cordova_options = {};
                cordova_options.timeout = 10000;
                cordova_options.chunkedMode = false;
                cordova_options.fileKey = "file";        
                cordova_options.fileName = dest_pic_name;               
                
                return $cordovaFileTransfer.upload(upload_host+upload_url_path, data, cordova_options, true)
                    .then(function(result) {                            
                        return {result:TRANSFER_SUCCESS,file_name:dest_pic_name,local_file_path:data};
                    }, function(err) {
                        alert('transfer FAILED');
                        return {result:TRANSFER_FAILED};
                    });                                        
            }, function(err){
                alert('aborted camera');
                return {result:CAMERA_FAILED};
            });            
        },
        TRANSFER_FAILED:TRANSFER_FAILED,
        TRANSFER_SUCCESS:TRANSFER_SUCCESS,
        CAMERA_FAILED:CAMERA_FAILED
    };    
}]);
