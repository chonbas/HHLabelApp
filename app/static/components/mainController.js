var HHLabelApp = angular.module('HHLabelApp', ['ngResource', 'ngMaterial','ngSanitize','ngRoute','ezfb', 'HHLabelApp.services']);

HHLabelApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/auth', {
                templateUrl: 'static/components/auth/authTemplate.html',
                controller: 'HHAuthController'
            }).
            when('/instructions', {
                templateUrl: 'static/components/instructions/instructionsTemplate.html',
                controller: 'HHInstructionsController'
            }).
            when('/home', {
                templateUrl: 'static/components/main_landing/main_landingTemplate.html',
                controller: 'HHMainLandingController'
            }).
            when('/stats', {
                templateUrl: 'static/components/stats/statsTemplate.html',
                controller: 'HHStatsController'
            }).
            otherwise({
                redirectTo: '/home'
            });
    }]);

HHLabelApp.controller('HHMainController', ['$scope', '$rootScope', '$location', '$resource',
    function($scope, $rootScope, $location, $resource){
        $scope.main = {};
        $scope.main.labeling = false;
        $scope.main.CheckLogin = $resource('/check');
        $scope.main.auth_status = false;
        $scope.main.active_user = "";
        $scope.main.Logout = $resource('/auth/logout');

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


        $scope.main.parseKeys = function(keyEvent){
            if ($scope.main.labeling){
                $scope.$broadcast('key-press', keyEvent);
            }
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
                            $location.path("/home");
                        }
                    }
            });                   
        });

    }]);