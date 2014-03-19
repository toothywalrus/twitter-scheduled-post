'use strict';

window.angular.module('Posting').directive('dashboard', function(Restangular, $rootScope) {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        templateUrl: 'dashboard.html',
        controller: function($scope, Info) {
            var watchAllChildren = function() {
                window.angular.forEach(Info.getChildResources(), function(name) {
                    $rootScope.$watchCollection('info.' + name, function() {
                        $rootScope.info_change = !$rootScope.info_change;
                    });
                });
            };
            $rootScope.loading = true;
            Info.retrieve().then(function(resp) {
                $rootScope.info = resp;
                $rootScope.info_change = false;
                watchAllChildren();
                $rootScope.loading = false;
            });
        }
    };
});