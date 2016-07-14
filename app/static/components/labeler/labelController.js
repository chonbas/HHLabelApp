 
HHLabelApp.controller('HHLabelController', ['$scope','$rootScope', '$resource','$http','$sanitize',
function($scope, $rootScope, $resource, $http, $sanitize){
    $scope.label = {};
    $scope.label.comment = {};
    $scope.label.comment.body = "";
    $scope.label.comment.id = "";
    $scope.label.comment.label = "";
    $scope.label.label_count = 0;
    $scope.label.GetNextComment = $resource('/getComment');
    $scope.label.SaveComment = $resource('/saveComment');

    $scope.$on('key-press', function(event, keyEvent){
        if (keyEvent.keyCode === 45){
            $scope.label.chooseNotHarass();
        } else if (keyEvent.keyCode === 61){
            $scope.label.chooseHarass();
        }
    });

    $scope.main.labeling = true;

    $scope.label.chooseHarass = function(){
        $scope.label.comment.label = true;
        $scope.label.pushComment();
    };

    $scope.label.chooseNotHarass = function(){
        $scope.label.comment.label = false;
        $scope.label.pushComment();
    };
    
    $scope.label.cycle = function(){
        $scope.label.GetNextComment.get()
            .$promise.then(function(comment){
                $scope.label.comment.body = comment.body;
                $scope.label.comment.id = comment.id;
                $scope.label.label_count = comment.count;
                if (comment.count % 10 === 0){
                    $rootScope.$broadcast('updateLeaders', 'updatingLeaders');
                    $rootScope.$broadcast('updateTotals', 'updatingTotals');  
                }
            }, function(err){
                $scope.label.comment.body = err.data;
            });
    };

    $scope.label.cycle();

    $scope.label.pushComment = function(){
        $scope.label.SaveComment.save({comment_id:$scope.label.comment.id, label:$scope.label.comment.label})
            .$promise.then(function(){
                $scope.label.cycle();
            }, function(err){
                $scope.label.comment.body = err.data;
                console.log(err);
            });
    };
}
]);
