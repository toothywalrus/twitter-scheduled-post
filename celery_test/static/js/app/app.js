'use strict';

var Posting = window.angular.module('Posting', ['ui.bootstrap', 'ngCookies', 'restangular', 'angular.directives-round-progress'], function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    }
);

Posting.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl('/tweets');
});

Posting.run(function($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});
