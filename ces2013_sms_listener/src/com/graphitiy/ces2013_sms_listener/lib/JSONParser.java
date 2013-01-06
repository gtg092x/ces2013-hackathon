package com.graphitiy.ces2013_sms_listener.lib;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.List;
 
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONException;
import org.json.JSONObject;
 
import android.util.Log;
 
public class JSONParser {
 
    static InputStream is = null;
    static JSONObject jObj = null;
    static String json = "";
 
    // constructor
    public JSONParser() {
 
    }
    
    public JSONObject getJSONFromUrl(String url){
    	return getJSONFromUrl(url, null, HttpMethod.GET);    	
    }
    
    public JSONObject getJSONFromUrl(String url, List<NameValuePair> params){
    	return getJSONFromUrl(url, params, HttpMethod.POST);    	
    }
 
    public JSONObject getJSONFromUrl(String url, List<NameValuePair> params,HttpMethod method) {
    
        // Making HTTP request
        try {
            // defaultHttpClient
            DefaultHttpClient httpClient = new DefaultHttpClient();
            HttpResponse httpResponse = null;
            switch(method){
            	case POST: 
            		HttpPost httpPost = new HttpPost(url);            
                    httpPost.setEntity(new UrlEncodedFormEntity(params)); 
                    httpResponse = httpClient.execute(httpPost);
            		break;
            	case PUT: 
            		HttpPut httpPut = new HttpPut(url);            
                    httpPut.setEntity(new UrlEncodedFormEntity(params)); 
                    httpResponse = httpClient.execute(httpPut);
            		break;
            	case DELETE: 
            		HttpDelete httpDelete = new HttpDelete(url);                                 
                    httpResponse = httpClient.execute(httpDelete);
            		break;
            	case GET: 
            		if(params!=null && params.size()>0){
            			if(url.indexOf("?")>0){
            				if(url.indexOf("?")!=url.length()-1){
            					url= url + "&";
            				}
            			}else{
            				url= url + "?";
            			}
            			url = url + new UrlEncodedFormEntity(params);
            		}
            		HttpGet httpGet = new HttpGet(url);            
            		
                    httpResponse = httpClient.execute(httpGet);
                    
            		break;
            	default:
            		return null;
            		
            }
            
            
            
            HttpEntity httpEntity = httpResponse.getEntity();
            is = httpEntity.getContent();
 
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(
                    is, "iso-8859-1"), 8);
            StringBuilder sb = new StringBuilder();
            String line = null;
            while ((line = reader.readLine()) != null) {
                sb.append(line + "n");
            }
            is.close();
            json = sb.toString();
            Log.e("JSON", json);
        } catch (Exception e) {
            Log.e("Buffer Error", "Error converting result " + e.toString());
        }
 
        // try parse the string to a JSON object
        try {
            jObj = new JSONObject(json);
        } catch (JSONException e) {
            Log.e("JSON Parser", "Error parsing data " + e.toString());
        }
 
        // return JSON String
        return jObj;
 
    }
    
    
}
