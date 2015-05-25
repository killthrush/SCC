'use strict';

define(['angularAMD', 'angular-route'], function (angularAMD) {

    var questionModule = angular.module('questionsApp', ['ngRoute']);

    questionModule.config(['$routeProvider', function($routeProvider) {
        $routeProvider.otherwise({redirectTo: '/mainView'});
    }]);

    questionModule.controller('questionsController', function($scope) {
        $scope.questionsList = [
            {
                question: 'Why doesn''t AngularJS support AMD modules?',
                answer: 'They didn''t want to.',
                distractors: [
                    'AMD modules weren''t invented yet.',
                    'AMD modules are evil.'
                    'Rick Astley.'
                ]
            },
            {
                question: 'Where did I put my keys?',
                answer: 'In my pocket.',
                distractors: [
                    'In the car.',
                    'On the shelf.'
                    'In the toaster.'
                ]
            },            
        ];
    });

    return angularAMD.bootstrap(questionModule);
});