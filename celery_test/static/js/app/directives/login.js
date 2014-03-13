'use strict';

angular.module('Posting').directive('login', function($http, $cookieStore, authService) {
    return {
        restrict: 'A',
        link: function(scope, elem, attrs) {
            elem.bind('submit', function() {
                var user_data = {
                    "username": scope.username,
                    "password": scope.password
                };

                $http.post(constants.serverAddress + "api-token-auth", user_data, {"Authorization": ""})
                    .success(function(response) {
                        $cookieStore.put('djangotoken', response.token);
                        $http.defaults.headers.common['Authorization'] = 'Token' + response.token;
                        authService.loginConfirmed();
                    });
            });
        }
    }
});