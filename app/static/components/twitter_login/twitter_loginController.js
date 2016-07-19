HHLabelApp.controller('HHTwitterController', ['$scope', '$q', '$resource', 'twitterService',
    function($scope, $q, $resource, twitterService) {
        twitterService.initialize();
        $scope.twitter = {};
        $scope.twitter.upload_status = false;
        $scope.twitter.tweets = []; //array of tweets
        $scope.twitter.cleaned = [];
        $scope.twitter.prev_id = 0;
        $scope.twitter.maxed = false;
        $scope.twitter.UploadTweets = $resource('/ingestTwitter');
        $scope.twitter.CheckTweets = $resource('/checkTwitter');

        //using the OAuth authorization result get as many tweets as possible before hitting the 
        //api limit / and/or running out of tweets to pull
        $scope.twitter.refreshTimeline = function(maxId) {
            if (!$scope.twitter.upload_status){
                twitterService.getLatestTweets(maxId).then(function(data) {
                    var temp = [].concat(data);
                    if ((typeof temp[temp.length -1]) !== 'undefined'){
                        if (temp[temp.length - 1].id === $scope.twitter.prev_id){
                            $scope.twitter.uploadTweets();
                        }
                        $scope.twitter.tweets = $scope.twitter.tweets.concat(data);
                        $scope.twitter.prev_id = $scope.twitter.tweets[$scope.twitter.tweets.length-1].id;
                        if ($scope.twitter.maxed !== true){
                            $scope.twitter.refreshTimeline($scope.twitter.prev_id);
                        }
                    } else{
                        $scope.twitter.uploadTweets();
                    }
                }, function() {
                    $scope.twitter.rateLimitError = true;
                    console.log("rateLimitError");
                });
            }
        };

        $scope.twitter.uploadTweets = function(){
            $scope.twitter.maxed = true;
            $scope.twitter.cleaned = $scope.twitter.tweets.map(function(tweet){
                var stripped_tweet = tweet.text.replace(/@\w+\s/, "@person ").replace(/RT\s:\s/, " ");
                var cleanedTweet = {'body':stripped_tweet};
                return cleanedTweet;
            });
            $scope.twitter.UploadTweets.save($scope.twitter.cleaned)
                .$promise.then(function(res){
                    $scope.twitter.uploaded = true;
                }, function(err){
                    console.log(err.data);
                });
            return;
        };

        $scope.twitter.checkTweets = function(){
            $scope.twitter.CheckTweets.get()
                .$promise.then(function(status){
                    $scope.twitter.upload_status = status.status;
                });
        };

        $scope.twitter.checkTweets();
        //when the user clicks the connect twitter button, the popup authorization window opens
        $scope.twitter.connectButton = function() {
            twitterService.connectTwitter().then(function() {
                if (twitterService.isReady()) {
                    //if the authorization is successful, hide the connect button and display the tweets
                    $('#connectButton').fadeOut(function() {
                        $('#getTimelineButton, #signOut').fadeIn();
                        $scope.twitter.refreshTimeline();
                        $scope.twitter.connectedTwitter = true;
                    });
                } else {

                }
            });
        }

        //sign out clears the OAuth cache, the user will have to reauthenticate when returning
        $scope.twitter.signOut = function() {
            twitterService.clearCache();
            $scope.twitter.tweets.length = 0;
            $('#getTimelineButton, #signOut').fadeOut(function() {
                $('#connectButton').fadeIn();
            });
            $scope.twitter.connectedTwitter = false;
            $scope.twitter.maxed = false;
            $scope.twitter.prev_id = 0;
        }

        //if the user is a returning user, hide the sign in button and display the tweets
        if (twitterService.isReady()) {
            $('#connectButton').hide();
            $('#getTimelineButton, #signOut').show();
            $scope.twitter.connectedTwitter = true;
            $scope.twitter.refreshTimeline();
        }
}]);