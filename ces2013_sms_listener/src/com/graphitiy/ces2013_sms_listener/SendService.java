package com.graphitiy.ces2013_sms_listener;


import java.util.Random;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.graphitiy.ces2013_sms_listener.lib.JSONParser;

import android.os.Handler;
import android.os.IBinder;
import android.R.integer;
import android.app.Service;
import android.content.Intent;
import android.telephony.SmsManager;
import android.util.Log;

public class SendService extends Service {
	private static final String TAG = "SendService";
	
	private int m_interval = 2000; // 2 seconds
	private Handler m_handler;
	
	@Override
	public IBinder onBind(Intent intent) {
		return null;
	}
	
	@Override
	public void onCreate() {
		//Toast.makeText(this, "My Service Created", Toast.LENGTH_LONG).show();
		Log.d(TAG, "onCreate");
		m_handler = new Handler();
		parser = new JSONParser();
		//player = MediaPlayer.create(this, R.raw.braincandy);
		//player.setLooping(false); // Set looping
	}
	
	Runnable m_statusChecker = new Runnable()
	{
	     @Override 
	     public void run() {
	          updateStatus(); //this function can change value of m_interval.
	          m_handler.postDelayed(m_statusChecker, m_interval);
	     }
	};
	private JSONParser parser;
	public void updateStatus(){
		Log.d(TAG,"Status");
		Random rand = new Random();
	    int salt = rand.nextInt(100000000);
		String url = "http://ces2013.graphitiy.com/api/outgoing-messages.json?nocache="+salt+"&$filter=sent%20ne%20True"; 
		JSONObject result = parser.getJSONFromUrl(url);
		if(result!=null){
			
			try {
				JSONArray messages = result.getJSONArray("results");
				for(int i=0;i<messages.length();i++){
					JSONObject message = (JSONObject) messages.get(i);
					String to_number = message.getString("to_number");
					String from_number = message.getString("from_number");
					String text_message = message.getString("message");
					
					SmsManager sms = SmsManager.getDefault();
			        sms.sendTextMessage(to_number, null, text_message, null, null);
				}				
				
			} catch (JSONException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}
		
	}

	@Override
	public void onDestroy() {
		//Toast.makeText(this, "My Service Stopped", Toast.LENGTH_LONG).show();
		Log.d(TAG, "onDestroy");
		m_handler.removeCallbacks(m_statusChecker);
		//player.stop();
	}
	
	@Override
	public void onStart(Intent intent, int startid) {
		//Toast.makeText(this, "My Service Started", Toast.LENGTH_LONG).show();
		Log.d(TAG, "onStart");
		m_statusChecker.run(); 
		//player.start();
	}
}
