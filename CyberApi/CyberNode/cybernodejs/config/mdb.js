/**
 * Created by CHASE BROWN on 4/21/2017.
 */
'use strict';

var mongoose = require('../node_modules/mongoose');
mongoose.connect("mongodb://cbrown:cyberarticles@ds159220.mlab.com:59220/cybernewsarticles");
var Articles =  mongoose.connection;
Articles.on('error', console.error.bind(console, 'connection error:'));
Articles.once('open', function(){
    //console.log('connected');
});

var Schema = mongoose.Schema;

var articleschema = new Schema({
    id:{type:String},
    uri:{type:String},
    date:{type:Date},
    author:{type:String},
    title:{type:String},
    body:{type:String},
    polarity:{type:Number},
    subjectivity:{type:Number}
},{collection:'articleinfo'});
module.exports = mongoose.model('articleinfo',articleschema);