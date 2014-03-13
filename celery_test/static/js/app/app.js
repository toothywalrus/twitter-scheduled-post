'use strict';

var Posting = window.angular.module('Posting', ['ui.bootstrap', 'ngCookies', 'restangular', 'ngQuickDate'], function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    }
);

Posting.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl('/tweets');
/*    RestangularProvider.addFullRequestInterceptor(function(element, operation, route, url, headers, params) {
        return {
            element: element,
            params: params,
            headers: _.extend(headers, {Authorization: 'Basic ' + 'sometoken'})
        };
    });*/


    /*return ngQuickDateDefaultsProvider.set({
        closeButtonHtml: "<i class='fa fa-times'></i>",
        buttonIconHtml: "<i class='fa fa-clock-o'></i>",
        nextLinkHtml: "<i class='fa fa-chevron-right'></i>",
        prevLinkHtml: "<i class='fa fa-chevron-left'></i>",
        // Take advantage of Sugar.js date parsing
        parseDateFunction: function(str) {
          d = Date.create(str);
          return d.isValid() ? d : null;
        }
    });*/
});

Posting.run(function($http, $cookies, $rootScope) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];

/*    var resolveDone = function () { $rootScope.doingResolve = false; };
 
    $rootScope.doingResolve = false;
 
    $rootScope.$on('$stateChangeStart', function () {
        $rootScope.doingResolve = true;
    });
 
    $rootScope.$on('$stateChangeSuccess', resolveDone);
    $rootScope.$on('$stateChangeError', resolveDone);
    $rootScope.$on('$permissionError', resolveDone);*/
});