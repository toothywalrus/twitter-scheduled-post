var Posting = angular.module("Posting");

var appController = Posting.controller('AppController', ['$scope', 'GlobalService', 'Tweet', 'TimedTweet', function($scope, GlobalService, Tweet, TimedTweet) {
    var failureCb = function (status) {
        console.log(status);
    };

    $scope.globals = GlobalService;

    $scope.initialize = function (is_authenticated) {
        $scope.globals.is_authenticated = is_authenticated;
    };

    $scope.tweets = [];
    $scope.newStatus = "";

    $scope.loadTweets = function () {
        return Tweet.query().$promise.then(function (results) {
            return $scope.tweets = results;
        });
    };

    $scope.addTweet = function () {
        var tweet;
        tweet = new Tweet({'status': $scope.newStatus});
        $scope.newStatus = "";
        return tweet.$save().then($scope.loadTweets);
    };

    $scope.deleteTweet = function (tweet) {
        return tweet.$delete().
        then($scope.loadTweets).
        then($scope.loadTimedTweets);

    };

    $scope.loadTweets();

    $scope.timedTweets = [];
    $scope.newTimedTweet = {
        tweet: null,
        post_time: new Date()
    };

    $scope.loadTimedTweets = function () {
        return TimedTweet.query().$promise.then(function (results) {
            return $scope.timedTweets = results;
        });
    };

    $scope.addTimedTweet = function () {
        var tweet = new TimedTweet($scope.newTimedTweet);
        $scope.newTimedTweet = {tweet: null, post_time: new Date()};
        return tweet.$save().then($scope.loadTimedTweets);
    };

    $scope.loadTimedTweets();


}]);