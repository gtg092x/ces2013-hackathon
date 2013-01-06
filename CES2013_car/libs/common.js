var Graphitiy = {};

Graphitiy.message_send = function(params,complete){
	
	var url="http://ces2013.graphitiy.com/api/outgoing-messages.json";
	
	gm.comm.webServiceRequest(complete, complete, 
	{url:url,method:"POST",parameters:params});
};

Graphitiy.message_poll = function(){
	var url = "http://ces2013.graphitiy.com/api/incoming-messages.json?$filter=viewed%20ne%20True";
	//url="http://ces2013.graphitiy.com/api/incoming-messages.json";
	gm.comm.webServiceRequest(function(obj){
		obj = JSON.parse(obj);
		
		if(obj.results){
			
			Graphitiy.message_poll.update(obj.results);
		}
		
	}, function(){
		console.log(arguments);
	}, {url:url});

};

Graphitiy.message_poll.onUpdate = function(){};

Graphitiy.message_poll.start = function(){

	Graphitiy.message_poll.stop();
	Graphitiy.message_poll.tid = setInterval(function(){
		Graphitiy.message_poll();		
	},2000);	

};

Graphitiy.message_poll.stop = function(){
	if(Graphitiy.message_poll.tid)
		clearInterval(Graphitiy.message_poll.tid);

};


Graphitiy.message_poll.update = function(messages){
	Graphitiy.message_poll.onUpdate(messages);
};


