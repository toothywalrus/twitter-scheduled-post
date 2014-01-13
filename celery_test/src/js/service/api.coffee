app = angular.module 'celery_test.api', ['ngResource']

app.factory 'Link', ['$resource', ($resource) ->
	$resource '/api/links/:id', id: '@id'
]

app.factory 'WebPage', ['$resource', ($resource) ->
	$resource '/api/webpages/:id', id: '@id'
]

app.factory 'Tweet', ['$resource', ($resource) ->
    $resource '/tweet_api/tweets/:id', id: '@id'
]