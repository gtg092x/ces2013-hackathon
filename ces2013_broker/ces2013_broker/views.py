from django.http import HttpResponse
import urllib2

def audio_proxy(request):
    
    
    accessToken = "xprtvphuqez7ougbbjtpsw05o96mpu2j";
    accessToken = "6ahmekcov40vr7i3vqd8brkjqifzynbv";
    url = "https://api.foundry.att.com/a1/speechalpha/texttospeech?access_token="+accessToken;
    
    text = request.GET.get("text","Hello World")
    
    #make a request object to hold the POST data and the URL
    request_object = urllib2.Request(url, text)
    
    #make the request using the request object as an argument, store response in a variable
    response = urllib2.urlopen(request_object)
    
    
    
    response = HttpResponse(response,content_type="audio/wav")
    
    return response;