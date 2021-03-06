HHLabelApp.controller('HHTwitterController', ['$scope', '$rootScope', '$q', '$resource', 'twitterService',
    function($scope, $rootScope, $q, $resource, twitterService) {
        twitterService.initialize();
        $scope.twitter = {};
        $scope.twitter.tweets = []; //array of tweets collected from api
        $scope.twitter.cleaned = []; //array of cleaned tweets to be ingested
        $scope.twitter.prev_id = 0; // variable used to monitor ids when pulling tweets from api
        $scope.twitter.score = null; // score on twitter
        $scope.twitter.harass_tweets = []; //array of tweets returned after ingestion/classificattion for user review
        $scope.twitter.active = {};
        $scope.twitter.show_tweets = false;
        $scope.twitter.pullingTweets = false;
        $scope.twitter.UploadTweets = $resource('/ingestTwitter');
        $scope.twitter.CheckTweets = $resource('/checkTwitter');


        $scope.twitter.checkTweets = function(){
            $scope.twitter.CheckTweets.get()
                .$promise.then(function(res){
                    $scope.twitter.score = res.score;
                });
        };

        $scope.twitter.checkTweets();

        //using the OAuth authorization result get as many tweets as possible before hitting the 
        //api limit / and/or running out of tweets to pull
        $scope.twitter.refreshTimeline = function(prev_id){
            console.log("pulling");
            twitterService.getLatestTweets(prev_id).then(function(data) {
                    var temp = [].concat(data);
                    //check to see if last payload from twitter api was undefined,
                    //ie. this checks to see if we already pulled all tweets available
                    if ((typeof temp[temp.length - 1])  === 'undefined'){
                        $scope.twitter.uploadTweets();
                        return;
                    }
                    //check to see if last payload was a repeat (this happens
                    //with accounts that have a small number of tweets)
                    if (temp[temp.length - 1].id === $scope.twitter.prev_id){
                        $scope.twitter.uploadTweets();
                        return;
                    }
                    //append new tweets, track last received id
                    $scope.twitter.tweets = $scope.twitter.tweets.concat(data);
                    $scope.twitter.prev_id = $scope.twitter.tweets[$scope.twitter.tweets.length-1].id;
                    $scope.twitter.refreshTimeline($scope.twitter.prev_id);
                }, function(err){
                    $scope.twitter.uploadTweets();
                    console.log('rateLimitError');
                });

        }

        $scope.twitter.pullTweets = function(){
            $scope.twitter.tweets = [];
            $scope.twitter.prev_id = 0;
            $scope.twitter.refreshTimeline();
        }

        $scope.twitter.uploadTweets = function(){
            console.log('uploading?');
            $scope.twitter.harass_tweets = [];
            console.log($scope.twitter.tweets);
            $scope.twitter.cleaned = $scope.twitter.tweets.map(function(tweet){
                var stripped_tweet = tweet.text.replace(/@\s*\w+\s/, "@person ").replace(/RT\s:\s/, " ");
                var cleanedTweet = {'body':stripped_tweet, 'id': tweet.id};
                return cleanedTweet;
            });
            if ($scope.twitter.tweets.length === 0){
                console.log('here');
                return;
            }
            $scope.twitter.UploadTweets.save($scope.twitter.cleaned)
                .$promise.then(function(res){
                    $scope.twitter.score = res.score;
                    $scope.twitter.harass_tweets = res.tweets;
                    if (res.tweets.length > 0){
                        $scope.twitter.active = {'index':0, 'body':res.tweets[0]};
                        $scope.twitter.show_tweets = true;
                    } else {
                        $scope.twitter.show_tweets = false;
                    }
                    console.log(res);
                }, function(err){
                    console.log(err.data);
                });
            return;
        };

        $scope.twitter.viewNextTweet = function(){
                var cur_index = $scope.twitter.active.index;
                if (cur_index === $scope.twitter.harass_tweets.length - 1){
                    cur_index = 0;
                } else {
                    cur_index++;
                }
                $scope.twitter.active = {'index':cur_index, 'body':$scope.twitter.harass_tweets[cur_index]};
        }


        //when the user clicks the connect twitter button, the popup authorization window opens
        $scope.twitter.connectButton = function() {
            twitterService.connectTwitter().then(function() {
                if (twitterService.isReady()) {
                    //if the authorization is successful, hide the connect button and display the tweets
                    $('#connectButton').fadeOut(function() {
                        $('#resyncButton, #signOut').fadeIn();
                        $scope.twitter.pullTweets();
                    });
                } else {

                }
            });
        }


        //sign out clears the OAuth cache, the user will have to reauthenticate when returning
        $scope.twitter.signOut = function() {
            twitterService.clearCache();
            $scope.twitter.tweets.length = 0;
            $('#resyncButton, #signOut').fadeOut(function() {
                $('#connectButton').fadeIn();
            });
            $scope.twitter.show_tweets = false;
            $scope.twitter.prev_id = 0;
        }

        $scope.twitter.checkService = function(){
            //if the user is a returning user, hide the sign in button and display the tweets
            if (twitterService.isReady()) {
                $('#connectButton').hide();
                $('#resyncButton, #signOut').show();
            }
        };

        $scope.twitter.checkService();

        $rootScope.$on('toggleTwitter', function(event, pass){
            $scope.twitter.checkService();
        });

}]);