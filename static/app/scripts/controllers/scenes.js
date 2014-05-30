define(['controllers/controllers','services/scenes'],
  function(controllers){
    controllers.controller('SceneCtrl', function ($scope, SceneService) {
      SceneService.getAllScenes().then(function(scenes) {
        console.log(scenes);
      })
    });
  }
);
