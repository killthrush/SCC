'use strict';

requirejs.config({

    appDir: ".",
    baseUrl: ".",
    paths: { 
        'jquery': ['http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min'],
        'bootstrap': ['http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min'],
        'angular': ['http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.min'],
        'angular-route': ['http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular-route.min'],
        'angularAMD': ['libs/angularAMD']
    },

    shim: {
        'bootstrap' : ['jquery'],
        'angularAMD': ['angular'], 
        'angular-route': ['angular']
    },

    deps: ['angularModule']
});

requirejs(['jquery', 'bootstrap', 'angular', 'angular-route', 'angularAMD'], function() {
    console.log("All modules loaded.");    
    return {};
});


