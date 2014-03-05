/**
 * Password collection page controller
 */
angular.module('tolkienControllers', [])
    .controller('PasswdCtrl', ['$scope', '$http', function($scope, $http){
        // Start by requesting a csrf token
        $http.get('http://107.170.228.214/auth/csrf')
            .success(function(data){
                console.log(data);
            });
    }]);