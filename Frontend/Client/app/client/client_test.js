'use strict';

describe('myApp.client module', function() {

  beforeEach(module('myApp.driver'));

  describe('driver controller', function(){

    it('should ....', inject(function($controller) {
      //spec body
      var view1Ctrl = $controller('View1Ctrl');
      expect(view1Ctrl).toBeDefined();
    }));

  });
});