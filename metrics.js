var MongoMetrics = require('mongo-metrics/bin/mongo-metrics');
var MONGODB_URL = "mongodb://127.0.0.1/soundlog";
var metrics = new MongoMetrics(MONGODB_URL);

//metrics.track('amps', 344, 'my-source', function(err) {});
metrics.aggregate('no-of-users', 'amp', 'avg', 'sum', {time: { $gte: 1161030882576 }}, function(err, result) {});
