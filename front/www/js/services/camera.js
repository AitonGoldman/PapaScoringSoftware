angular.module('TD_services.camera',[]);
angular.module('TD_services.camera').factory('Camera', ['$state','$timeout','$rootScope',function($state,$timeout,$rootScope) {            
    var dest_pic_name="1.jpg";
    var upload_host="http://98.111.232.93:8000";
    var upload_url_path="/test/media_upload/user_pic";

    var upload_url=function(){
        return upload_host+upload_url_path;
    };
    
    var upload_success = function (r) {
        alert('Uploaded success!');
        console.log("Code = " + r.responseCode);
        console.log("Response = " + r.response);
        console.log("Sent = " + r.bytesSent);
        //$http.get('http://98.111.232.93/pics/1.jpg');
        //$state.go('event_select');
        };

    var upload_fail = function (error) {
        alert('Upload failed');
        console.log("upload error source " + error.source);
        console.log("upload error target " + error.target);
    };
        
    var cameraSuccess = function(pic_path){
        var options = new FileUploadOptions();
        options.trustAllHosts = true;
        options.chunkedMode = false;            
        options.fileKey = "file";        
        options.fileName = dest_pic_name;               
        var params = {};
        params.app_name = "test";
        options.params = params;        
        var ft = new FileTransfer();        
        ft.upload(pic_path, encodeURI(upload_url()), upload_success, upload_fail, options);
    };
    return{
        take_user_pic_and_upload:function(user_id){
            dest_pic_name=user_id+".jpg";
            var upload_host="http://98.111.232.93:8000";
            var upload_url_path="/test/media_upload/user_pic";
            navigator.camera.getPicture(cameraSuccess, cameraSuccess, {});
        }        
    };
    
}]);
