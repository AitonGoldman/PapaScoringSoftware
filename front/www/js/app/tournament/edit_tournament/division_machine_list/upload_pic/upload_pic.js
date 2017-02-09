angular.module('app.tournament.edit_tournament.division_machine_list.upload_pic',[/*REPLACEMECHILD*/]);
angular.module('app.tournament.edit_tournament.division_machine_list.upload_pic').controller(
    'app.tournament.edit_tournament.division_machine_list.upload_pic',[
        '$scope','$state','TimeoutResources','Utils','Modals','$http',
        function($scope, $state, TimeoutResources, Utils,Modals,$http) {
        $scope.site=$state.params.site;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.uploadedFile = function(element) {
            console.log('in uploadedFiled');
            $scope.$apply(function($scope) {
                console.log('in uploadedFiled apply');
                $scope.files = element.files;         
            });
        };
            $scope.renameUploadedFile = function(){
                Modals.loading();
                upload_promise = TimeoutResources.AddBackglassPic(undefined,{site:$scope.site,division_machine_id:$scope.division_machine_id},{pic_file:$scope.uploaded_pic_name});
                upload_promise.then(function(data){
                    Modals.loaded();
                    $state.go('.^');
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
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
