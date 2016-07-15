HHLabelApp.controller('HHTwitterController', ['$scope','$resource', 'youtubeService',
    function($scope, $resource, youtubeService) {
        youtubeService.initialize();
}]);