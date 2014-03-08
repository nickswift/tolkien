/**
 * Tolkien API connection Service
 */
angular.module('tolkienServices', [])
    .factory('tolkienAPI', ['$http', function($http){
            var api_url = 'http://107.170.228.214/api';
            return {
                // Ask the server to rotate the CSRF token
                // and store it in the csrf cookie
                get_csrf: function(){
                    return $http({
                        method: 'GET',
                        url   : api_url + '/auth/csrf'
                    });
                },
                // login and logout requests
                login: function(csrf, username, password){
                    return $http({
                        method: 'POST',
                        url   : api_url + '/auth/user/login',
                        data  : {
                            'username':username,
                            'password':password
                        },
                        headers: {
                            'X-CSRFToken'  : csrf,
                            'Content-Type' : 'application/json'
                        }
                    });
                },
                logout: function(csrf, stoken){
                    return $http({
                        method: 'POST',
                        url   : api_url + '/auth/user/logout',
                        data  : {
                            'stoken': stoken
                        },
                        headers: {
                            'X-CSRFToken'  : csrf,
                            'Content-Type' : 'application/json'
                        }
                    });
                }
            };
        }]);