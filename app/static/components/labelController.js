var HHLabelApp = angular.module('HHLabelApp', ['ngResource', 'ngSanitize','ezfb']);
// .config(function(ezfbProvider){
//     ezfbProvider.setInitParams({
//         appId      : '1046357475402235'
//     });
// });

HHLabelApp.controller('HHLabelController', ['$scope','$rootScope', '$resource','$http','$sanitize', 'ezfb',
function($scope, $rootScope, $resource, $http, $sanitize, ezfb){
    $scope.main = {};
    $scope.main.comment = {};
    $scope.main.comment.body = "";
    $scope.main.comment.id = "";
    $scope.main.comment.label = "";
    // $scope.main.fb = {};
    // $scope.main.fb.response = "";
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
                $scope.main.label_count = comment.count;
                $rootScope.$broadcast('updateLeaders', 'updatingLeaders');
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

    // $scope.main.syncFB = function(){
    //     ezfb.login(function(res) {
    //         ezfb.api('/me?fields=posts', function (res_api) {
    //             console.log(res_api);
    //         });
    //     }, {scope:'email, user_posts'});
    // };
}
]);
