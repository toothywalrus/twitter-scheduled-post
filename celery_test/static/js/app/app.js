'use strict';

var Posting = window.angular.module('Posting', ['ui.bootstrap', 'ngCookies', 'restangular', 'ngQuickDate'], function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    }
);

Posting.config(function(RestangularProvider, ngQuickDateDefaultsProvider) {
    RestangularProvider.setBaseUrl('/tweets');
    return ngQuickDateDefaultsProvider.set({
        closeButtonHtml: "<i class='fa fa-times'></i>",
        buttonIconHtml: "<i class='fa fa-clock-o'></i>",
        nextLinkHtml: "<i class='fa fa-chevron-right'></i>",
        prevLinkHtml: "<i class='fa fa-chevron-left'></i>",
        // Take advantage of Sugar.js date parsing
        parseDateFunction: function(str) {
          d = Date.create(str);
          return d.isValid() ? d : null;
        }
    });
});

Posting.run(function($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});