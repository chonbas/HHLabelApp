HHLabelApp.config(function(ezfbProvider){
    ezfbProvider.setInitParams({
        appId      : '1046357475402235'
    });
});

HHLabelApp.controller('HHFBLoginController', ['$scope', '$rootScope', '$resource',
    function ($scope, $rootScope, $resource) {
        $scope.fblogin = {};
        $scope.fblogin.CheckFB = $resource('/checkfb') 
        $scope.fblogin.collected = false;

        $scope.fblogin.checkFBCollect = function(){
            $scope.fblogin.CheckFB.get()
                .$promise.then(function(fbstatus){
                    $scope.fblogin.collected = fbstatus.status;
                }, function(err){
                    console.log(err);
                });
        };

        $scope.fblogin.checkFBCollect();
}]);