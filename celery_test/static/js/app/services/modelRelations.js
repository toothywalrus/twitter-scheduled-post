angular.module('Posting').factory('modelRelations', function() {
    return {
        tweet: {
            child: 'timedTweet',
            parent: null,
        },
        postTweetSet: {
            child: 'periodicTweet',
            parent: null,
            name: 'tweetset'
        },
        periodicTweet: {
            child: null,
            parent: 'postTweetSet'
        },
        timedTweet: {
            child: null,
            parent: 'tweet'
        }
    };
});