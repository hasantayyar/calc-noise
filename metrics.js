var MongoMetrics = require('mongo-metrics');
//var MONGODB_URL = "mongodb://127.0.0.1/soundlog";
//var metrics = new MongoMetrics(MONGODB_URL);
//metrics.aggregate('hits', 'amp', 'avg', 'sum', {time: { $gte: 1161030882576 }}, function(err, result) {});
var dashboard = require('mongo-metrics/dashboard');

var MONGO_URL = "mongodb://localhost/soundlog";
var PORT = 5005;
dashboard.listen(MONGO_URL, PORT);
