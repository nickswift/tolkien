/**
 * Password collection page controller
 */
angular.module('tolkienControllers', [])
    .controller('PasswdCtrl', ['$scope', '$http', function($scope, $http){
        // API connection and login values
        var api_url     = 'http://107.170.228.214/api',
            api_headers = null,
            csrf        = null,
            stoken      = null;

        // Metadata collection values
        $scope.dt_last_keystroke     = 0;
        $scope.md_keystroke_times    = [];
        $scope.md_keystroke_time_sum = 0;
        $scope.md_backspaces         = 0;

        // Start by requesting a csrf token
        $http.get(api_url + '/auth/csrf')
            .success(function(data){
                console.log('csrf', data);
                csrf        = data;
                api_headers = {
                    'X-CSRFToken' : data,
                    'Content-Type': 'application/json'
                };
            });

        // Sign a user up for the service 
        // TODO: Prune users on a set interval
        $scope.signup = function(){
            if(!csrf){ return; }

            $http({
                method: 'POST',
                url   : api_url + '/auth/user/create',
                data  : {
                    'username': $scope.username,
                    'password': $scope.password
                },
                headers: api_headers
            })
            .success(function(data){
                console.log('Signed up');
            });
        };

        // Log the user in
        // TODO: supply Metadata
        $scope.login = function(){
            if(!csrf){ return; }

            $http({
                method: 'POST',
                url   : api_url + '/auth/user/login',
                data  : {
                    'username': $scope.username,
                    'password': $scope.password
                },
                headers: api_headers
            })
            .success(function(data){
                // Set the session token
                stoken = data.stoken;
                logout();
            });
        };

        // on password keypress, start/continue the metadata collection process
        $scope.collect_md = function(e){
            // TODO: collect backspaces, and quit if that's the case
            console.log(e);

            // If this is the first keystroke, just set up the system to get the
            // next one.
            if(!$scope.dt_last_keystroke){
                $scope.dt_last_keystroke = new Date().getTime();
                return;
            }
            // record time since last keystroke
            var now = new Date().getTime();
            $scope.md_keystroke_times.push({
                time: now-$scope.dt_last_keystroke
            });

            // summate keystroke times
            $scope.md_keystroke_time_sum = 0;
            for(var i=0;i<$scope.md_keystroke_times.length;i++){
                $scope.md_keystroke_time_sum += $scope.md_keystroke_times[i].time;
            }

            // console.log($scope.md_keystroke_times, $scope.md_keystroke_time_sum);

            // Set up the next keystroke
            $scope.dt_last_keystroke = now;
        };

        // Use session token to log the user out -- this gets called 
        // automatically, since there's nothing this service actually does
        function logout(){
            if(!stoken){ return; }
            $http({
                method: 'POST',
                url   : api_url + '/auth/user/logout',
                data  : {
                    'stoken': stoken
                },
                headers: api_headers
            })
            .success(function(data){
                console.log('Success! ', data);
                stoken = null;
            });
        }
    }]);