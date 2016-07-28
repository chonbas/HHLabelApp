HHLabelApp.controller('HHLeaderboardController', ['$scope', '$rootScope', '$resource',
    function ($scope, $rootScope, $resource) {
        $scope.leaderboard = {};
        $scope.leaderboard.leaderboard = [];
        $scope.leaderboard.time_updated = new Date().toUTCString();
        $scope.leaderboard.GetLeaderboard = $resource('/leaderBoard');

        $scope.leaderboard.updateLeaders = function(){
            $scope.leaderboard.GetLeaderboard.get()
                .$promise.then(function(leaderlist){
                    $scope.leaderboard.leaderboard = leaderlist.leaders;
                    $scope.leaderboard.time_updated = new Date().toUTCString();
                }, function(err){
                    console.log(err.data);
                });
        };

        $scope.leaderboard.updateLeaders();

        $rootScope.$on('updateLeaders', function(event, pass){
            $scope.leaderboard.updateLeaders();
        });
}]);