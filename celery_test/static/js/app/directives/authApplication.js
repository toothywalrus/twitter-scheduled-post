'use strict';

angular.module('Posting').directive('authApplication', function($cookieStore, $http) {
    return {
        restrict: 'A',
        link: function(scope, elem, attrs) {
            var login = elem.find('#login-holder');
            var main = elem.find('#main');

            scope.$on('event:auth-loginRequired', function() {
                main.hide();
                login.slideDown('fast');
            });

            scope.$on('event:auth-loginConfirmed', function() {
                main.show();
                login.slideUp('fast');
            });

            scope.$on('event:initial-auth', function() {
                if ($cookieStore.get('djangotoken')) {
                    $http.defaults.headers.common['Authorization'] = 'Token' + $cookieStore.get('djangotoken');
                }
                else {
                    login.slideDown('fast');
                    main.hide();
                }
            });
        }
    }
});