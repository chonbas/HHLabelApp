HHLabelApp.controller('HHTotalsController', ['$scope', '$rootScope', '$resource',
    function ($scope, $rootScope, $resource) {
        $scope.totals = {};
        $scope.totals.total_count = 0;
        $scope.totals.harass_count = 0;
        $scope.totals.comment_count = 0;
        $scope.totals.time_updated = new Date().toUTCString();
        $scope.totals.GetTotals = $resource('/totals');

        $scope.totals.updateTotals = function(){
            $scope.totals.GetTotals.get()
                .$promise.then(function(totals_obj){
                    $scope.totals.label_count = totals_obj.total_labels;
                    $scope.totals.harass_count = totals_obj.harass_labels;
                    $scope.totals.comment_count = totals_obj.total_comments;
                    $scope.totals.time_updated = new Date().toUTCString();
                }, function(err){
                    console.log(err.data);
                });
        };

        $scope.totals.updateTotals();

        $rootScope.$on('updateTotals', function(event, pass){
            $scope.totals.updateTotals();
        });
}]);