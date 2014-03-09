/**
 * Tolkien API connection Service
 */
angular.module('tolkienServices', [])
    .factory('tolkienAPI', ['$http', '$cookies', function($http, $cookies){
            var api_url = '/api';

            return {
                // Ask the server to rotate the CSRF token
                // and store it in the csrf cookie
                get_csrf: function(){
                    return $http({
                        method: 'GET',
                        url   : api_url + '/auth/csrf'
                    });
                },

                // sign up
                signup: function(csrf, username, password){
                    return $http({
                        method : 'POST',
                        url    : api_url + '/auth/user/create',
                        data   : {
                            'username' : username,
                            'password' : password
                        },
                        headers: {
                            'X-CSRFToken'  : csrf,
                            'Content-Type' : 'application/json'
                        }
                    });
                },

                // login and logout requests
                login: function(csrf, username, password){

                    console.log('connecting with ', csrf);
                    return $http({
                        method: 'POST',
                        url   : api_url + '/auth/user/login',
                        data  : {
                            'username' : username,
                            'password' : password
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