package com.graphitiy.ces2013_sms_listener;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.graphitiy.ces2013_sms_listener.lib.JSONParser;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.telephony.SmsMessage;
import android.util.Log;

public class SmsListener extends BroadcastReceiver{

	static final String ACTION ="android.provider.Telephony.SMS_RECEIVED";
    private SharedPreferences preferences;
    private JSONParser parser;
    
    public void PostMessage(String from, String text_message){
    	
    	String url = "http://ces2013.graphitiy.com/api/incoming-messages.json";
    	ArrayList<NameValuePair> params = new ArrayList<NameValuePair>();
    	params.add(new BasicNameValuePair("to_number","4046677975"));
    	params.add(new BasicNameValuePair("from_number",from));
    	params.add(new BasicNameValuePair("message",text_message));
		JSONObject result = parser.getJSONFromUrl(url,params);
		
    	
    }
    
    @Override
    public void onReceive(Context context, Intent intent) {
        // TODO Auto-generated method stub
    	parser = new JSONParser();
    	Log.d("SmsListener","Received");
        if(intent.getAction().equals(ACTION)){
            Bundle bundle = intent.getExtras();           //---get the SMS message passed in---
            SmsMessage[] msgs = null;
            String msg_from;
            if (bundle != null){
                //---retrieve the SMS message received---
                try{
                    Object[] pdus = (Object[]) bundle.get("pdus");
                    msgs = new SmsMessage[pdus.length];
                    for(int i=0; i<msgs.length; i++){
                        msgs[i] = SmsMessage.createFromPdu((byte[])pdus[i]);
                        msg_from = msgs[i].getOriginatingAddress().replace("+1", "");
                        String msgBody = msgs[i].getMessageBody();
                        
                        PostMessage(msg_from,msgBody);
                        
                    }
                }catch(Exception e){
//                            Log.d("Exception caught",e.getMessage());
                }
            }
        }
    }
}