/**
 * Tolkien: password metadata collection
 * -- the frontend application
 */
angular.module('tolkienApp', [
        'ngRoute',
        'tolkienControllers'
    ])
    .config(['$routeProvider', function($routeProvider){
        $routeProvider
            .when('/', {
                templateUrl: 'res/views/password.html',
                controller : 'PasswdCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    }]);