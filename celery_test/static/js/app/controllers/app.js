'use strict';

window.angular.module('Posting').controller('AppController', function($scope) {
    $scope.$on('info:start_load', function() {
        $scope.loading = true;
    });

    $scope.$on('info:stop_load', function() {
        $scope.loading = false;
    });
});