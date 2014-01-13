var api = angular.module('celery_test.api', ['ngResource']);

api.factory('Tweet', ['$resource', function ($resource) {
    return $resource('/tweets/tweets/:id', {id: '@id'});
}]);

api.factory('TimedTweet', ['$resource', function ($resource) {
    return $resource('/tweets/timedtweets/:id', {id: '@id'});
}]);