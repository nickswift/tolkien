/**
 * Password collection page controller
 */
angular.module('tolkienControllers', [])
    .controller('PasswdCtrl', ['$scope', '$http', 'tolkienAPI',
        function($scope, $http, tolkienAPI){

            // Non-scope values
            var csrf = {
                    exists : false,
                    token  : null
                },
                metadata = {
                    ks_prev     : 0,
                    ks_times    : [],
                    ks_total    : 0,
                    prev_length : 0
                };

            // Rotate the csrf token on the server, and grab the new one
            // from that server
            function attain_csrf(){
                csrf.exists = false;
                tolkienAPI.get_csrf()
                    .success(function(token){
                        csrf.exists = true;
                        csrf.token  = token;
                        console.log(csrf);
                    });
            }

            // Scope values
            _.assign($scope, {
                username       : null,
                password       : null,
                hiw_visible    : false,
                metadata       : null,
                successful_pws : [],
                failed_pws     : [],

                reset_password: function(){
                    $scope.password = null;
                    metadata = {
                        ks_prev     : 0,
                        ks_times    : [],
                        ks_total    : 0,
                        prev_length : 0
                    };
                },
                signup: function(){
                    if(!csrf.exists){ return; }

                    tolkienAPI
                        .signup(csrf.token, $scope.username, $scope.password)
                        .success(function(data){
                            console.log('signed up');
                        });
                },
                login: function(){
                    if(!csrf.exists){ return; }
                    
                    tolkienAPI
                        .login(csrf.token, $scope.username, $scope.password)
                        .success(function(data){
                            console.log('login success!', 'logging out...');
                            $scope.successful_pws.push(metadata);
                            $scope.reset_password();
                            $scope.logout(data.stoken);
                        })
                        .error(function(data){
                            $scope.reset_password();
                            $scope.failed_pws.push(metadata);
                        });
                },
                logout: function(stoken){
                    if(!csrf.exists){ return; }
                    tolkienAPI.logout(csrf.token, stoken)
                        .success(function(){
                            attain_csrf();
                        });
                },
                toggle_hiw_visible: function(){
                    $scope.hiw_visible = !$scope.hiw_visible;
                }
            });

            // Password watcher
            $scope.$watch('password', function(){
                var now = new Date().getTime();
                // Update password metadata
                if(!$scope.password){ return; }
                // Kill password on backspace
                if($scope.password.length < metadata.prev_length){
                    $scope.reset_password();
                    return;
                }
                // if this is the first letter, get process started
                if(!metadata.ks_prev){
                    metadata.ks_prev = new Date().getTime();
                    return;
                }
                metadata.ks_times.push({
                    time: now - metadata.ks_prev
                });
                metadata.ks_total = 0;
                for(var i=0;i<metadata.ks_times.length;i++){
                    metadata.ks_total += metadata.ks_times[i].time;
                }
                // setup next keystroke
                metadata.ks_prev     = now;
                metadata.prev_length = $scope.password.length;

                // Keep scope metadata current
                $scope.metadata = metadata;

                console.log(metadata);
            });
        
            // request CSRF after the view is done loading
            $scope.$on('$viewContentLoaded', function(){
                attain_csrf();
            });
        }]);