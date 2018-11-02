  app.controller('upload', function($scope,$window,Upload,$http,$location) {
    $scope.cardfinished = false;
    $scope.filename = ""
    $scope.uploadfile=function(files,cardname){
        console.log(files)
        if(files!=null){
            Upload.upload({
                url: '/api/upload',
                method:'POST',
                data:{data:{card:$scope.newcardnameBack,value:''},files:files}
            }).success(function (resp) {
                console.log(resp);
                $scope.filename = resp;
                $scope.cardfinished=true;
            }, function (resp) {
                console.log('Error status: ' + resp.status);
            }, function (evt) {
                var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file.name);
            }).finally(function(){
                $scope.cardfinished=true;
            });
        }else {
            console.log(cardname);
            $scope.uploaderror = "Please select your pan card file to upload";
        }
    }
    $scope.getText = function(){
        //console.log($scope.filename)
        $http.post('/api/ocrdata', {"filename": $scope.filename})
        .then(function(response){
            var text = response.data;
            $scope.data = text.split('\n');
            console.log(data);
        })
    }
  });
