HHLabelApp.controller('HHAuthController', ['$scope', '$rootScope', '$resource', '$location',
    function ($scope, $rootScope, $resource, $location) {
        $scope.auth = {};
        $scope.auth.register = false;

        $scope.auth.username = "";
        $scope.auth.password = "";
        $scope.auth.password2 = "";
        $scope.auth.email = "";
        $scope.auth.error = "";
        $scope.auth.remember_me = false;

        $scope.auth.Login = $resource('/api/login');
        $scope.auth.Register = $resource('/api/register');


        $scope.auth.attemptLogin = function(){
            if ($scope.auth.email === "" || $scope.auth.password === ""){
                $scope.auth.error = "Please enter a username and password.";
                return;
            }
            var loginAttempt = {email:$scope.auth.email, password: $scope.auth.password, remember_me:$scope.auth.remember_me};
            $scope.auth.Login.save(loginAttempt)
                .$promise.then(function(res){
                    if (!res.status){
                        $scope.auth.error = "Invalid email or password.";
                        return;
                    } else{
                        $scope.main.auth_status = res.status;
                        $scope.main.active_user = res.user;
                        $location.path("/instructions");
                    }
                });
        };

        $scope.auth.attemptRegister = function(){
            if ($scope.auth.email.length === 0 || $scope.auth.username.length === 0){
                $scope.auth.error = "Please enter a username and email address."
                return;
            }
            if ($scope.auth.password.length <= 3){
                $scope.auth.error = "Password must be longer than 4 characters.";
                return;
            }
            if ($scope.auth.password !== $scope.auth.password2){
                $scope.auth.error = "Ensure passwords match.";
                return;
            }
            var registerAttempt = {email: $scope.auth.email,
                                    password: $scope.auth.password,
                                    username: $scope.auth.username};
            $scope.auth.Register.save(registerAttempt)
                .$promise.then(function(res){
                    if (res.status !== 'success'){
                        $scope.auth.error = res.status;
                        return;
                    } else {
                        $scope.auth.error = "Registration successful."
                        $scope.auth.toggleView();
                    }
                });

        };

        $scope.auth.toggleView = function(){
            $scope.auth.register = !$scope.auth.register;
        }

}]);