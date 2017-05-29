angular.module('app.finals_scorekeeper',['app.finals_scorekeeper.division_final',
                                         /*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper').controller(
    'app.finals_scorekeeper',[
        '$scope','$state','TimeoutResources','Utils','Modals',
        function($scope, $state, TimeoutResources, Utils,Modals) {
            $scope.site=$state.params.site;
            $scope.resources = {};
            $scope.utils = Utils;
            Modals.loading();
            async.waterfall([
                function(callback){                    
                    TimeoutResources.GetDivisionFinals({site:$scope.site},undefined,callback);
                }],function(err,result){
                Modals.loaded();
                if (err == null){
                    $scope.resources[result.resource_name] = result;                    
                    //$scope.resources = Utils.extract_results_from_response(result);
                } else {
                    console.log(err);                                
                }
            });
            
        }]
);
