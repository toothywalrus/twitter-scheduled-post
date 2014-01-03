app = angular.module 'celery_test.app.editor', ['celery_test.api', 'celery_test.app.basic']

app.controller 'EditController', ['$scope', 'Link', 'WebPage', ($scope, Link, WebPage) ->
	$scope.newPage = new WebPage()
	$scope.save = ->
		$scope.newPage.$save().then (result) ->
			$scope.pages.push result
		.then ->
			$scope.newPage = new WebPage()
		.then ->
			$scope.errors = null
		, (rejection) ->
			$scope.errors = rejection.data
]