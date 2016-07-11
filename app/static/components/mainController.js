var HHLabelApp = angular.module('HHLabelApp', ['ngResource', 'ngMaterial','ngSanitize','ngRoute','ezfb']);

HHLabelApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/auth', {
                templateUrl: 'static/components/auth/authTemplate.html',
                controller: 'HHAuthController'
            }).
            when('/label', {
                templateUrl: 'static/components/labeler/labelerTemplate.html',
                controller: 'HHLabelController'
            }).
            when('/instructions', {
                templateUrl: 'static/components/instructions/instructionsTemplate.html',
                controller: 'HHInstructionsController'
            }).
            otherwise({
                redirectTo: '/instructions'
            });
    }]);

HHLabelApp.controller('HHMainController', ['$scope', '$rootScope', '$location', '$resource',
    function($scope, $rootScope, $location, $resource){
        $scope.main = {};
        $scope.main.CheckLogin = $resource('/check');
        $scope.main.auth_status = false;
        $scope.main.active_user = "";
        $scope.main.Logout = $resource('/api/logout');

        $scope.main.attemptLogout = function(){
            $scope.main.Logout.get()
                .$promise.then(function(res){
                        $scope.main.auth_status = false;
                        $scope.main.active_user = "";
                        $location.path("/auth");
                });
        };

        $scope.main.checkAuthStatus = function(){
            $scope.main.CheckLogin.get()
                .$promise.then(function(res){
                    $scope.main.auth_status = res.status;
                    $scope.main.active_user = res.user;
                });
        };



        $rootScope.$on( "$routeChangeStart", function(event, next, current) {
             $scope.main.CheckLogin.get()
                .$promise.then(function(res){
                    $scope.main.auth_status = res.status;
                    $scope.main.active_user = res.user;
                    if (!$scope.main.auth_status) {
                        // no logged user, redirect to /auth unless already there
                        if (next.templateUrl !== "static/components/auth/authTemplate.html") {
                            $location.path("/auth");
                        }
                        return;
                    } else {
                        if (next.loadedTemplateUrl === "static/components/auth/authTemplate.html") {
                            $location.path("/instructions");
                        }
                    }
            });                   
        });

    }]);