package com.graphitiy.ces2013_sms_listener;


import android.os.Handler;
import android.os.IBinder;
import android.app.Service;
import android.content.Intent;
import android.content.IntentFilter;
import android.util.Log;

public class ReceiveService extends Service {
	static final String SMS_ACTION ="android.provider.Telephony.SMS_RECEIVED";
	private static final String TAG = "ReceiveService";
	
	private int m_interval = 1000; // 1 second
	private Handler m_handler;
	
	@Override
	public IBinder onBind(Intent intent) {
		return null;
	}
	
	@Override
	public void onCreate() {

		Log.d(TAG, "onCreate");
		
	    
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
	
	public void updateStatus(){
		Log.d(TAG,"Status");
	}

	@Override
	public void onDestroy() {
		//Toast.makeText(this, "My Service Stopped", Toast.LENGTH_LONG).show();
		Log.d(TAG, "onDestroy");
		
		//player.stop();
	}
	
	@Override
	public void onStart(Intent intent, int startid) {
		//Toast.makeText(this, "My Service Started", Toast.LENGTH_LONG).show();
		Log.d(TAG, "onStart");
		//IntentFilter filter = new IntentFilter();
	    //filter.addAction(SMS_ACTION);
	    //this.registerReceiver(new SmsListener(), filter);
		//player.start();
	}
}
