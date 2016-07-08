var HHLabelApp = angular.module('HHLabelApp', ['ngResource', 'ngSanitize','ezfb']);


HHLabelApp.controller('HHLabelController', ['$scope','$rootScope', '$resource','$http','$sanitize',
function($scope, $rootScope, $resource, $http, $sanitize){
    $scope.main = {};
    $scope.main.comment = {};
    $scope.main.comment.body = "";
    $scope.main.comment.id = "";
    $scope.main.comment.label = "";
    $scope.main.label_count = 0;
    $scope.main.GetNextComment = $resource('/getComment');
    $scope.main.SaveComment = $resource('/saveComment');

    $scope.main.parseKeys = function(keyEvent){
        if (keyEvent.keyCode === 45){
            $scope.main.chooseNotHarass();
        } else if (keyEvent.keyCode === 61){
            $scope.main.chooseHarass();
        }
    };

    $scope.main.chooseHarass = function(){
        $scope.main.comment.label = true;
        $scope.main.pushComment();
    };

    $scope.main.chooseNotHarass = function(){
        $scope.main.comment.label = false;
        $scope.main.pushComment();
    };
    
    $scope.main.cycle = function(){
        $scope.main.GetNextComment.get()
            .$promise.then(function(comment){
                $scope.main.comment.body = comment.body;
                $scope.main.comment.id = comment.id;
                $scope.main.label_count = comment.count;
                if (comment.count % 10 === 0){
                    $rootScope.$broadcast('updateLeaders', 'updatingLeaders');
                    $rootScope.$broadcast('updateTotals', 'updatingTotals');  
                }
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
    };
}
]);
