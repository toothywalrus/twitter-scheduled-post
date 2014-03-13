'use strict';

angular.module('Posting').filter('capitalize', function () {
    return function (input) {
        return input.charAt(0).toUpperCase() + input.slice(1);
    };
});