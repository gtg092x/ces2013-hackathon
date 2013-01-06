function GUID ()
{
    var S4 = function ()
    {
        return Math.floor(
                Math.random() * 0x10000 /* 65536 */
            ).toString(16);
    };

    return (
            S4() + S4() + "-" +
            S4() + "-" +
            S4() + "-" +
            S4() + "-" +
            S4() + S4() + S4()
        );
}



var MessageModel = {message:{},accept:function(msg){
	var exists = MessageModel.message&&MessageModel.message.id==msg.id;
	
	MessageModel.message=msg;
	if(!exists){
		
		View.showResponses(msg);
	}
}};

var ContextModel={clear:function(){
	this.request=false;
	this.mode=false;
}};

var ResponseModel = {responses:{},add:function(response){
	var exists = !!ResponseModel.responses[response.id];
	ResponseModel.responses[response.id]=response;
	if(View.state=="RESPONSES" && !exists)
		View.appendResponse(response.id);
	
}};

ResponseModel.genResponses = function(message){
	
	ResponseModel.responsesFromMessage(message,
		ResponseModel.act
		
	);
};

ResponseModel.act = function(responses){
	ResponseModel.responses = responses;
	var contextMessages = ResponseModel.responsesFromContext(ContextModel.context);
	if(contextMessages)
		ResponseModel.responses = ResponseModel.responses.concat(contextMessages);
	ResponseModel.responses = ResponseModel.responses.concat(ResponseModel.defaultResponses());
	
	for(var i =0;i<ResponseModel.responses.length;i++){
		var id = GUID();
		ResponseModel.responses[i].id=id;
		ResponseModel.responses[id]=ResponseModel.responses[i];
	}
	View.clear(function(){
		View.draw();
	});
};

var Model = {response:ResponseModel,message:MessageModel,context:ContextModel}; 

var View = {state:"WAITING"};

View.draw = function(){
	
	if(View.state=="WAITING")
		View.drawWaiting();
	else
		View.drawResponses();
		
	$('.fadeInRight').removeClass('fadeInRight').removeClass('fadeOutRight').addClass('fadeInRight');
	$('.fadeInLeft').removeClass('fadeInLeft').removeClass('fadeOutLeft').addClass('fadeInLeft');
	$('.fadeInUp').removeClass('fadeInUp').removeClass('fadeOutUp').addClass('fadeInUp');
	$('.fadeIn').removeClass('fadeIn').removeClass('fadeOut').addClass('fadeIn');
};

View.clear = function(callback){
	$('.fadeInRight').removeClass('fadeInRight').addClass('fadeOutRight');
	$('.fadeInLeft').removeClass('fadeInLeft').addClass('fadeOutLeft');
	$('.fadeInUp').removeClass('fadeInUp').addClass('fadeOutUp');
	$('.fadeIn').removeClass('fadeIn').addClass('fadeOut');
	var wait = window.setTimeout( function(){
			callback();},
			500
	);
};

View.drawResponses = function(){
	
	var response_html = "";
	
	
	var template = _.template(
            $( "script#responses_template" ).html()
        );
    $("#canvas").html(
		template( {} )
	);
	for(var i=0;i< ResponseModel.responses.length;i++){
		View.appendResponse(ResponseModel.responses[i],i);		
	}
	
	$("#message").html(
		Model.message.message.message
	);
	$("#sender").html(
		"from <span id='from'>"+Model.message.message.from_number+"</span>:"
	);
};

View.drawWaiting = function(){
	
	
	var template = _.template(
            $( "script#waiting_template" ).html()
        );
    $("#canvas").html(
		template( {} )
	);
};



View.getChoiceResponseHtml = function(response,i){
	var template = _.template(
            $( "script#response_choice_template" ).html()
        );
    var ind = String.fromCharCode(97 + i).toUpperCase();
    response.ind = ind;
    //var body = response;
	return	template({response:response});	
};


View.showResponses = function(message_id){
	
		
	View.state="RESPONSES";
	ResponseModel.genResponses(MessageModel.message);
	
};

View.showWaiting = function(){
	
	MessageModel.message=null;	
	View.state="WAITING";
	View.clear(function(){
		View.draw();
	});
	
};

 
View.appendResponse = function(response,i){
	
	$("#responses").append(
		View.getChoiceResponseHtml(response,i)
	);
	
	$("#response_"+response.id,"#responses").bind("click",function(){
		var id = $(this).data("pk");
		var response =ResponseModel.responses[id]; 
		var body = response.content;
		
		Graphitiy.message_send({message:body,to_number:Model.message.message.from_number,from_number:Model.message.message.to_number},
		function(){
			View.showWaiting();
		});
		if(response.onClick)
			response.onClick();
		else
			Model.context.clear();
	}).data("pk",response.id);
};

//only fires when there are new messages
Graphitiy.message_poll.onUpdate = function(messages){
	
	if(messages.length)
		MessageModel.accept(messages[messages.length-1]);
};

ResponseModel.defaultResponses = function(message){
	
	return [		
		{type:"system",label:"(it can wait)",content:"I can't answer right now, I'm driving. I can get back to you in x minutes."}
	];
};

ResponseModel.responsesFromContext = function(context){
	if(ContextModel.request)
		return;
	responses = [];
		if(!ContextModel.mode||ContextModel.mode!="list")
		responses.push({label:"(Ask for List)",content:"Can you give me a list of choices?",type:"system",
			onClick:function(){
				Model.context.request="list";
			}});
		if(!ContextModel.mode||ContextModel.mode!="yesorno")
		responses.push({label:"(Ask for yes or no)",content:"Can this be a yes or no question?",type:"system",
			onClick:function(){
				Model.context.request="bool";
			}});
	return responses;
};

ResponseModel.guessKeywords = function(message){
	return message.message.search(/where.{0,50}((food)|(restaurant)|(eat)|(breakfast)|(dinner))/i)>-1;
};

ResponseModel.timeKeywords = function(message){
	return message.message.search(/(when)|(how long)|(time)/i)>-1;
};

ResponseModel.responsesFromMessage = function(message,callback){
	if(ResponseModel.guessKeywords(message))
		return ResponseModel.guess(message,callback);
	
	if(ResponseModel.timeKeywords(message)){
		callback(ResponseModel.timeResponses());
	}else if(Model.context.request=="bool"){
		callback(ResponseModel.yesOrNoResponses());
	}else if(Model.context.request=="list" || 
		(message.message.trim().match(/(or)|(and)/g)||[]).length){
		callback(ResponseModel.listFromMessage(message.message));
	}else{
		ResponseModel.guess(message,callback);
	}
	
};

ResponseModel.timeResponses = function(){
	ContextModel.mode="time";
	return [
				{label:"1 hour",content:"1 hour from now",type:"gen"},
				{label:"30 minutes",content:"30 minutes from now",type:"gen"},
				{label:"15 minutes",content:"15 minutes from now",type:"gen"},
				{label:"10 minutes",content:"10 minutes from now",type:"gen"}				
			];
};

ResponseModel.yesOrNoResponses = function(){
	ContextModel.mode="yesorno";
	
	return [
				{label:"Yes",content:"Yes",type:"gen"},
				{label:"No",content:"No",type:"gen"},
				{label:"Ok",content:"Ok",type:"gen"}
			];
};

ResponseModel.listFromMessage = function(message){
	
	
	var i = message.trim().search(/\?.+/);
	if(i>-1){
		message = message.substring(i+1,message.length).trim().replace(/\?$/,"");
	};
	
	if(message.search(",")==-1)
		return ResponseModel.yesOrNoResponses();
	ContextModel.mode="list";
	message = message.replace(/,\s*((or)|(and))/,",",",");
	message = message.replace(/\s*,\s*/g,",");
	choices = message.split(",");
	var messages = [];
	for(var i =0;i<choices.length;i++){
		var capped = choices[i].substring(0,1).toUpperCase()+choices[i].substring(1,choices[i].length);
		messages.push({label:capped,content:choices[i],type:"gen"});
	};
	return messages;
};

ResponseModel.guess = function(message,callback){
	
	
	gm.info.getCurrentPosition(function(pos){
		responses = ResponseModel.yesOrNoResponses();
		callback(responses);
		return;
		var key = "AIzaSyCFMWMt-81s5MX69-8cwj1a-0o-X30JHuc";
		
		var minute_multiplier=10000000.0;
		var coords = (pos.coords.latitude/minute_multiplier)+","+(pos.coords.longitude/minute_multiplier);
		coords="36.071302,-115.135551";
		var placesUrl ="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+coords+"&radius=1000&types=food&sensor=false&key="+key;
		console.log(pos);
		console.log(placesUrl);
		gm.comm.webServiceRequest(function(obj){
			obj = JSON.parse(obj);
			
			responses = ResponseModel.yesOrNoResponses();
			
			
			
			callback(responses);
			
		}, function(){
			console.log(arguments);
		}, {url:placesUrl});
			
	}, callback);

};

function init()
{
	// TODO Add your code here
	
	View.showWaiting();
	Graphitiy.message_poll.start();
	
}
