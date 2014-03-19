'use strict';

window.angular.module('Posting').directive('selectAdd', function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: 'selectAdd.html',
        transclude: true,
        scope: {
            type: '@modelName',
        }
    };
});