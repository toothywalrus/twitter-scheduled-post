'use strict';

var Posting = angular.module("Posting", ["ui.bootstrap", "ui.bootstrap.datetimepicker", "ngCookies", "celery_test.api"], function ($interpolateProvider) {
        $interpolateProvider.startSymbol("{[{");
        $interpolateProvider.endSymbol("}]}");
    }
);

Posting.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});