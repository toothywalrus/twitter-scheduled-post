'use strict';

window.angular.module('Posting').directive('listItem', function($compile, $http, $templateCache) {
    var getTemplate = function(contentType) {
        var templateUrl = contentType + '-item.html';
        var templateLoader = $http.get(templateUrl, {cache: $templateCache});

        return templateLoader;
    };

    var linker = function(scope, element, attrs, listItemCtrl) {
        var loader = getTemplate(scope.type);

        loader.success(function(html) {
            element.html(html);
        }).then(function(response) {
            var newElem = $compile(element.html())(scope);
            element.replaceWith(newElem);
        });


    };

    var ctrl = function($scope) {
    };

    return {
        restrict: 'A',
        scope: {
            item: '=',
            type: '@'
        },
        link: linker,
        controller: ctrl
    };
});