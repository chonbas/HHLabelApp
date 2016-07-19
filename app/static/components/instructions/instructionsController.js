 
HHLabelApp.controller('HHInstructionsController', ['$scope','$rootScope', '$resource','$location',
function($scope, $rootScope, $resource, $location){
    $scope.instructions = {};
    $scope.instructions.viewShown = 1;

    $scope.instructions.setView = function(index){
        $scope.instructions.view = "/static/components/instructions/panes/instructions" + index +".html";
    };

    $scope.instructions.setView($scope.instructions.viewShown);

    $scope.instructions.nextView = function(){
        $scope.instructions.viewShown++;
        $scope.instructions.setView($scope.instructions.viewShown);
   };

    $scope.instructions.prevView = function(){
        $scope.instructions.viewShown--;
        $scope.instructions.setView($scope.instructions.viewShown); 
    };

    $scope.instructions.endView = function(){
        $scope.instructions.setView($scope.instructions.viewShown);
        $location.path("/home");
    };

}]);
