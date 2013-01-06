package com.graphitiy.ces2013_sms_listener;

import java.util.ArrayList;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONObject;

import com.graphitiy.ces2013_sms_listener.R;
import com.graphitiy.ces2013_sms_listener.lib.JSONParser;

import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.Button;

public class MainActivity extends Activity {
	private static final String TAG = "MainActivity";
	private JSONParser parser;
	
	public void PostMessage(String from, String text_message){
		parser = new JSONParser();
    	String url = "http://ces2013.graphitiy.com/api/incoming-messages.json";
    	ArrayList<NameValuePair> params = new ArrayList<NameValuePair>();
    	params.add(new BasicNameValuePair("to_number","4046677975"));
    	params.add(new BasicNameValuePair("from_number",from));
    	params.add(new BasicNameValuePair("message",text_message));
		JSONObject result = parser.getJSONFromUrl(url,params);
		
    	
    }
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
	    View.OnClickListener listener = new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				activityOnClick(view);
			}
		};
	    findViewById(R.id.SendOn).setOnClickListener(listener);
	    findViewById(R.id.SendOff).setOnClickListener(listener);
	    findViewById(R.id.receive_on).setOnClickListener(listener);
	    findViewById(R.id.ReceiveOff).setOnClickListener(listener);
	    
		
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.activity_main, menu);
		return true;
	}
	
	public void activityOnClick(View src) {
		Log.d(TAG, "onClick: "+src.getId());
	    switch (src.getId()) {
	    case R.id.receive_on:
	      Log.d(TAG, "onClick: starting receiver");
	      startService(new Intent(this, ReceiveService.class));
	      break;
	    case R.id.ReceiveOff:
	      Log.d(TAG, "onClick: stopping receiver");
	      stopService(new Intent(this, ReceiveService.class));
	      break;
	    case R.id.SendOn:
		      Log.d(TAG, "onClick: starting sender");
		      startService(new Intent(this, SendService.class));
		      break;
		case R.id.SendOff:
		      Log.d(TAG, "onClick: stopping sender");
		      stopService(new Intent(this, SendService.class));
		      break;
	    }
	  }

}
