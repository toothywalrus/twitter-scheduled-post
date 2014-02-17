'use strict';

window.angular.module('Posting').factory('GlobalService', function () {
    var vars = {
        is_authenticated: false
    };

    return vars;
});