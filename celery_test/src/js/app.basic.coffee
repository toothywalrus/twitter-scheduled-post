app = angular.module 'celery_test.app.basic', ['celery_test.api']

app.controller 'AppController', ['$scope', 'Link', 'WebPage', ($scope, Link, WebPage) ->
	$scope.links = Link.query()
	$scope.pages = WebPage.query()
]