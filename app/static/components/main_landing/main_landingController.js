HHLabelApp.controller('HHMainLandingController', ['$scope', '$rootScope', '$resource',
    function ($scope, $rootScope, $resource) {
        $scope.landing = {};
        $scope.landing.viewShown = "Label";
        $scope.landing.label = true;
        $scope.landing.twitter = false;

        $scope.landing.toggleLabel = function(){
            $scope.landing.label = true;
            $scope.landing.twitter = false;            
        };

        $scope.landing.toggleTwitter = function(){
            console.log("works");
            $scope.landing.label = false;
            $scope.landing.twitter = true;            
        };

}]);