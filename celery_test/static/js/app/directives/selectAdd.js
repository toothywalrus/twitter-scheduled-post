'use strict';

angular.module('Posting').directive('selectAdd', function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: 'selectAdd.html',
        transclude: true,
        scope: {
            modelName: '@',
        }
    };
});