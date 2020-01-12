'use strict';
module.exports = function(app) {
  var sequenceController = require('../controllers/sequenceController');

  app
  .get('/v1/sequence/gene/id/:id', sequenceController.sequenceInfoById)
  .get('/v1/sequence/id/:id', sequenceController.exportToFormat)
  .get('/', sequenceController.home)
};