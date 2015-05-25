'use strict';

define(['angularAMD', 'angular-route'], function (angularAMD, angularRoute) {

    var questionModule = angular.module('questionsApp', ['ngRoute']);

    questionModule.config(['$routeProvider', function($routeProvider) {
        $routeProvider.otherwise({redirectTo: '/mainView'});
    }]);

    questionModule.factory('questionService', function($http) {
        var api = {
            filterText: null
        };
        api.setQuestionFilter = function(filterText) {
            this.filterText = filterText;
        };
        api.getQuestions = function(onSuccess, onFailure) {
            var baseUrl = 'http://localhost:5000/questions/';

            var questionFilter = this.filterText ? 'qf=' + this.filterText : '';

            var query = '?' + questionFilter;

            var httpCall = $http({
                    method: 'GET', 
                    url: baseUrl + query
                });
            httpCall.success(onSuccess);
            return httpCall;
        };
        return api;
    });

    questionModule.controller('questionsController', function($scope, questionService) {
        $scope.questionsList = [];
        questionService.setQuestionFilter('100');
        var questionSource = questionService.getQuestions(function (response) {
            $scope.questionsList = response;
        });
    });

    return angularAMD.bootstrap(questionModule);
});