angular.module('Posting').factory('modelRelations', function() {

    var tree = {
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

    function getParent(modelName) {
        var pt = tree[modelName].parent;
        pt = (pt) ? (tree[pt].name || pt) : (null);
        return pt;
    }

    return angular.extend(tree, {getParent: getParent});
});