/*
 * JavaScript file
 */

function init()
{
	// TODO Add your code here
	
	gm.comm.webServiceRequest(function(){
		console.log(arguments);
	}, function(){
		console.log(arguments);
	}, {url:"http://ces2013.graphitiy.com/api/outgoing-messages.json"});
	
}
