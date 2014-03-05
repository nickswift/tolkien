/**
 * Tolkien: password metadata collection
 * -- the frontend application
 */
angular.module('tolkienApp', [
        'ngRoute',
        'tolkienControllers'
    ])
    .config(['$routeProvider', '$httpProvider',
        function($routeProvider, $httpProvider){
            /*
            $httpProvider.defaults.useXDomain = true;
            delete $httpProvider.defaults.headers.common['X-Requested-With'];
            */
            
            $routeProvider
                .when('/', {
                    templateUrl: 'res/views/password.html',
                    controller : 'PasswdCtrl'
                })
                .otherwise({
                    redirectTo: '/'
                });
        }]);