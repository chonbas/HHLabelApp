/*
-----------------------------------------------
HH Authentication Controller (HHAuthController):
-----------------------------------------------
AngularJS Controller associated with authTemplate.html

Utilized to handle logins/registrations on client.
Registers API endpoints needed for authentication as resources, 
and defines methods needed to interact with the api.

Includes both login and registration forms/controls.
-------------------------------------------------
*/
HHLabelApp.controller('HHAuthController', ['$scope', '$rootScope', '$resource', '$location',
    function ($scope, $rootScope, $resource, $location) {
        // We define the scope variables associated with this module 
        // using the #scope.auth path to ensure we don't have conflicts in the namespace.
        $scope.auth = {};
        $scope.auth.register = false;

        $scope.auth.username = "";
        $scope.auth.password = "";
        $scope.auth.password2 = "";
        $scope.auth.email = "";
        $scope.auth.error = "";
        $scope.auth.remember_me = false;

        //API endpoint registration as Angular $resoruces
        $scope.auth.Login = $resource('/auth/login');
        $scope.auth.Register = $resource('/auth/register');


        /*-------------------------------- 
        * $scope.auth.attemptLogin():
        *---------------------------------
        * Checks to make sure password and email fields are not blank,
        * if they are not, creates JSON that encapsulates form data 
        # and forwards it to the back-end as a POST request. 
        # We utilize the .$pomise.then() paradigm to enforce
        # that we wait for a response before moving on.
        # Upon a successful response from the server,
        # if a user is not a returning user we forward them to instructions/tutorial page.
        * if a user is a returning user, we forward them to the main landing.
        */
        $scope.auth.attemptLogin = function(){
            if ($scope.auth.email === "" || $scope.auth.password === ""){
                $scope.auth.error = "Please enter a username and password.";
                return;
            }
            var loginAttempt = {email:$scope.auth.email, password: $scope.auth.password, remember_me:$scope.auth.remember_me};
            $scope.auth.Login.save(loginAttempt)
                .$promise.then(function(res){
                    //check to ensure login was successul
                    if (!res.status){
                        $scope.auth.error = "Invalid email or password.";
                        return;
                    } else{
                        //Login was successul:
                        $scope.main.auth_status = res.status;
                        $scope.main.active_user = res.user;
                        //new user:
                        if (!res.return){
                            $location.path("/instructions");
                        //returning user:
                        } else {
                            $location.path("/home");
                        }
                        
                    }
                });
        };

        //-----------------------------------------------
        //$scope.auth.attemptRegister()
        //-----------------------------------------------
        // Function used to attempt user registration.
        // First we perform some error checking:
        // is a username and email entered?
        // is the password longer than 3 characters?
        // does the password confirmation match the original password?
        // if all checks pass, then create JSON to forward to back-end with form data.
        // If successful, display succesful registration message and display Login form
        // else indicate error  message (username taken etc)
        ///-----------------------------------------------
        $scope.auth.attemptRegister = function(){
            //error checking
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
            //collect form data into JSON
            var registerAttempt = {email: $scope.auth.email,
                                    password: $scope.auth.password,
                                    username: $scope.auth.username};
            //send POST request to back-end
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

        //Simple method used to toggle views between the login and registration form
        $scope.auth.toggleView = function(){
            $scope.auth.register = !$scope.auth.register;
        }

}]);