var HHLabelApp = angular.module('HHLabelApp', ['ngResource'])

HHLabelApp.controller('HHLabelController', ['$scope', '$resource','$http',
function($scope, $resource, $http){
    $scope.main = {};
    $scope.main.comment = {};
    $scope.main.comment.body = "";
    $scope.main.comment.id = "";
    $scope.main.comment.label = "";
    $scope.main.GetNextComment = $resource('/getComment');
    $scope.main.SaveComment = $resource('/saveComment');


    $scope.main.chooseHarass = function(){
        $scope.main.comment.label = 'Harassment'
        $scope.main.pushComment();
    };

    $scope.main.chooseNotHarass = function(){
        $scope.main.comment.label = 'Acceptable'
        $scope.main.pushComment();
    };
    
    $scope.main.cycle = function(){
        $scope.main.GetNextComment.get()
            .$promise.then(function(comment){
                $scope.main.comment.body = comment.body;
                $scope.main.comment.id = comment.id;
            }, function(err){
                $scope.main.comment.body = err.data;
            });
    };

    $scope.main.cycle();

    $scope.main.pushComment = function(){
        $scope.main.SaveComment.save({comment_id:$scope.main.comment.id, label:$scope.main.comment.label})
            .$promise.then(function(){
                $scope.main.cycle();
            }, function(err){
                $scope.main.comment.body = err.data;
                console.log(err);
            });
    }
}
]);
