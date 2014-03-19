'use strict';

var Posting = window.angular.module('Posting', ['ui.bootstrap', 'ngCookies', 'restangular', 'ngQuickDate', 'underscore', 'ngRoute'], function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    }
);

Posting.controller('AppController', function($scope, $http, streamService) {
    
    $scope.date = new Date();

});

Posting.config(function(RestangularProvider, $routeProvider) {
    RestangularProvider.setBaseUrl('/tweets');

    $routeProvider.when('/', {
        templateUrl: 'main.html',
        contoller: 'AppController'
    });

});

Posting.run(function($http, $cookies, $rootScope, streamService) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];

    $rootScope.data = "dfdfdf";

});

angular.module('underscore', []).factory('_', function() {
    return window._;
});
