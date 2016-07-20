HHLabelApp.controller('HHMainLandingController', ['$scope', '$rootScope', '$resource',
    function ($scope, $rootScope, $resource) {
        $scope.landing = {};
        $scope.landing.viewShown = "Label";
        $scope.landing.label = true;
        $scope.landing.twitter = false;
        $scope.landing.stats = false;

        $scope.landing.toggleLabel = function(){
            $scope.landing.label = true;
            $scope.landing.twitter = false;
            $scope.landing.stats = false;                        
        };

        $scope.landing.toggleTwitter = function(){
            $scope.landing.label = false;
            $scope.landing.twitter = true;
            $scope.landing.stats = false;            
        };

        $scope.landing.toggleStats = function(){
            $scope.landing.label = false;
            $scope.landing.twitter = false;
            $scope.landing.stats = true;
        }



}]);