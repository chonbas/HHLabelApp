HHLabelApp.controller('HHLeaderboardController', ['$scope', '$rootScope', '$resource',
    function ($scope, $rootScope, $resource) {
        $scope.leaderboard = {};
        $scope.leaderboard.total_count = 0;
        $scope.leaderboard.harass_count = 0;
        $scope.leaderboard.leaderboard = [];
        $scope.leaderboard.time_updated = Date();
        $scope.leaderboard.GetLeaderboard = $resource('/leaderBoard');

        $scope.leaderboard.updateLeaders = function(){
            $scope.leaderboard.GetLeaderboard.get()
                .$promise.then(function(leaderlist){
                    $scope.leaderboard.leaderboard = leaderlist.leaders;
                    $scope.leaderboard.total_count = leaderlist.total;
                    $scope.leaderboard.harass_count = leaderlist.harass;
                    $scope.leaderboard.time_updated = Date();
                }, function(err){
                    console.log(err.data);
                });
        };

        $scope.leaderboard.updateLeaders();

        $rootScope.$on('updateLeaders', function(event, pass){
            $scope.leaderboard.updateLeaders();
        });
}]);