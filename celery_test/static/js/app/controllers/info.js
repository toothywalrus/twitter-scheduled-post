'use strict';

window.angular.module('Posting').controller('InfoCtrl', function ($scope) {

    var source = new window.EventSource('/stream/');

    source.addEventListener('info', function (e) {
        var obj = JSON.parse(e.data);
        window.console.log(obj.resource_name);
    });

    $scope.info = 'smt';
});

