var app = angular.module('ocr', []);
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{[');
    $interpolateProvider.endSymbol(']}]');
});
app.controller('dashboardCtrl', function($scope, $http) {
    $scope.getUserDetials = function(){
        $http.get("/api/userData")
        .then(function(response) {
            $scope.userData = response.data;
            console.log($scope.userData);
        });
    }
    $scope.getUserDetials();
    $scope.updateKey = function(){
        $http.get("/api/updateKey")
        .then(function(response) {
            $scope.getUserDetials();
        });
    }
});