//---------------------------------------
//
// Alexei:
// Halting development on this to focus on twitter/google integration. 
// Will revisit upon having a more concrete language model that we can use
// In order to record a screen cast of the app to submit to FB
// To request user_posts permissions.
//
//----------------------------------------


HHLabelApp.config(function(ezfbProvider){
    ezfbProvider.setInitParams({
        appId      : '1046357475402235'
    });
});

HHLabelApp.controller('HHFBLoginController', ['$scope', '$rootScope', '$resource', 'ezfb',
    function ($scope, $rootScope, $resource, ezfb) {
        $scope.fblogin = {};
        $scope.fblogin.CheckFB = $resource('/checkfb') 
        $scope.fblogin.collected = false;

        $scope.fblogin.checkFBCollect = function(){
            $scope.fblogin.CheckFB.get()
                .$promise.then(function(fbstatus){
                    $scope.fblogin.collected = fbstatus.status;
                }, function(err){
                    console.log(err);
                });
        };

        $scope.fblogin.checkFBCollect();

        $scope.fblogin.collectFB = function(){
            ezfb.login(function(response){
                if (response.status === 'connected') {
                // Logged into your app and Facebook.
                    console.log(response);
                } else if (response.status === 'not_authorized') {
                // The person is logged into Facebook, but not your app.
                    console.log('not auth');
                } else {
                    console.log('not auth not logged to fb');
                // The person is not logged into Facebook, so we're not sure if
                // they are logged into this app or not.
                }
            }, {scope: 'user_posts'});
        };

}]);