angular.module('HHLabelApp.services', []).factory('twitterService', function($q) {

    var authorizationResult = false;

    return {
        initialize: function() {
            //initialize OAuth.io with public key of the application
            OAuth.initialize('i80pywmnQt-eA0sMc3fv40eRAJI', {
                cache: true
            });
            //try to create an authorization result when the page loads,
            // this means a returning user won't have to click the twitter button again
            authorizationResult = OAuth.create("twitter");
        },
        isReady: function() {
            return (authorizationResult);
        },
        connectTwitter: function() {
            var deferred = $q.defer();
            OAuth.popup("twitter", {
                cache: true
            }, function(error, result) {
                // cache means to execute the callback if the tokens are already present
                if (!error) {
                    authorizationResult = result;
                    deferred.resolve();
                } else {
                    //do something if there's an error
                    console.log(error);
                }
            });
            return deferred.promise;
        },
        clearCache: function() {
            OAuth.clearCache('twitter');
            authorizationResult = false;
        },
        getLatestTweets: function(maxId) {
            //create a deferred object using Angular's $q service
            var deferred = $q.defer();
            var url = '/1.1/statuses/user_timeline.json';
            if (maxId) {
                url += '?trim_user=true&include_rts=false&max_id=' + maxId;
            }
            var promise = authorizationResult.get(url).done(function(data) {
                // https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline
                // when the data is retrieved resolve the deferred object
                deferred.resolve(data);
            }).fail(function(err) {
                deferred.reject(err);
            });
            //return the promise of the deferred object
            return deferred.promise;
        }
    }
}).factory('youtubeService', function($q) {

    var authorizationResult = false;

    return {
        initialize: function() {
            gapi.load('client')
                .$promise.then(function(){
                    gapi.client.setApiKey('AIzaSyCm_wRobb69W8wTpp3CcXDNH6jsc6y-ckM');
                    authorizationResult =true;
                    return;
                });            
        },
        isReady: function() {
            return (authorizationResult);
        },
        getComments: function(channelID) {
            return gapi.client.request({
                'path': 'youtube/v3/youtube.commentThreads.list',
                'params': {'part':'snippet, replies',
                            'allThreadsRelatedToChannelId':channelID}
            });
        }
    }
});