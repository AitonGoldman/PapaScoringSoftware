angular.module('prereg.step1.step2.step3.step4',['prereg.step1.step2.step3.step4.step5',
    /*REPLACEMECHILD*/]);
angular.module('prereg.step1.step2.step3.step4').controller(
    'prereg.step1.step2.step3.step4',[
        '$scope','$state','TimeoutResources','Utils','Modals','$http',
        function($scope, $state, TimeoutResources, Utils,Modals,$http) {
            $scope.site=$state.params.site;
	    $scope.linked_division_id=$state.params.linked_division_id;
            dev_info = ionic.Platform.device();            
            if (_.size(dev_info)!=0){
                $scope.is_native=true;          
            }                
            
        $scope.utils = Utils;
        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
            $scope.server_ip_address=server_ip_address;
            $scope.http_prefix=http_prefix;
            $scope.server_port=server_port;
            

        $scope.uploadedFile = function(element) {
            console.log('in uploadedFiled');
            $scope.$apply(function($scope) {
                console.log('in uploadedFiled apply');
                $scope.files = element.files;         
            });
        };
        $scope.addFile = function() {
            console.log('in addfile');
            $scope.uploadfile($scope.files,
                                     function( msg ) // success
                              {
                                  console.log('in addfile - success');
                                  console.log('uploaded');
                              },
                              function( msg ) // error
                              {
                                  console.log('in addfile - failure');                                  
                                  console.log('error');
                              });
        };
        $scope.uploadfile = function(files,success,error){
            Modals.loading();
            var url = $scope.http_prefix+'://'+$scope.server_ip_address+':'+$scope.server_port+'/'+$scope.site+'/test/media_upload';

            for ( var i = 0; i < files.length; i++)
            {
                var fd = new FormData();
                fd.append("file", files[i]);
                console.log(files[i]);
                $http.post(url, fd, { 
                    withCredentials : false,
                    headers : {
                        'Content-Type' : undefined
                    },
                    transformRequest : angular.identity

                }).success(function(data){
                    console.log('success!');
                    console.log(data);
                    $scope.uploaded_pic_name=data.poop;
                    Modals.loaded();

                }).error(function(data){
                    console.log('uh oh!');                    
                    console.log(data);
                    Modals.loaded();
                });
            }
        };
    }]
);
