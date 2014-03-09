/**
 * Tolkien: password metadata collection
 * -- the frontend application
 */
angular.module('tolkienApp', [
        'ngRoute',
        'ngCookies',
        'tolkienControllers',
        'tolkienServices'
    ])

    .config(['$routeProvider', '$httpProvider',
        function($routeProvider, $httpProvider){
            $routeProvider
                .when('/', {
                    templateUrl: 'res/views/password.html',
                    controller : 'PasswdCtrl'
                })
                .otherwise({
                    redirectTo: '/'
                });
        }]);