import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

//TO DO:
//  1. Catch reason for failure and log it
//  2. Refactor for common HTTP method
//  3. Refactor for better code reuse
// 

public class petStoreApiTests{
	    
	static final String SERVERNAME = "http://petstore.swagger.io/v2";
	//static final String SERVERPORT = "80";
	
    public static void main(String[] args) {
        boolean skip = false;
        ArrayList<String> passedTests = new ArrayList<String>();
        ArrayList<String> failedTests = new ArrayList<String>();
	    
        try {
            String response="";
			//TO DO: be smarter on loop size for API commands
			for (int i=0; i<=1; i++){
			   String testName= "default";
			   String testURL = "http://petstore.swagger.io/v2";
			   //URL url = new URL("http://petstore.swagger.io/v2");
			   switch(i){
			      case 0:   
				     skip = false;
				     testName = "Get store inventory";
			         // Create a URL Connection, and get the store inventory
                     testURL = "http://petstore.swagger.io/v2/store/inventory";
					 break;
					 
				  case 1:
				     skip = false;
				     testName = "User Login";
					 testURL = "http://petstore.swagger.io/v2/user/login";
					 
					 //TO DO: pass in password credentials
					 //TO DO: finish the rest of the api calls
					 break;
				  default:
					 System.out.println("ERROR: unsupported test, skipping");
					 skip = true;
					 break;
			   }
               if (skip == false){			   
                  //System.out.println(url+"\n");
				  URL url = new URL(testURL);
                  HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                  conn.setDoOutput(true);
                  conn.setDoInput(true);
				  //TO DO: update method according to api
                  conn.setRequestMethod("GET");
                  conn.setUseCaches(false);
                  conn.setRequestProperty("Content-type", "text/xml");
                  conn.setRequestProperty("Connection", "Keep-Alive");

                  // Read the response.
                  BufferedReader rdr = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                  while (true) {
                      String str = rdr.readLine();
                      if (str == null) {
                          break; // We're done
                      }
                      System.out.println("****************** RESPONSE ***********************/n/n");
					  System.out.println(str);
					  System.out.println("****************** END RESPONSE ********************/n/n");
			   	      if (str != null && !str.isEmpty()){
                         passedTests.add(testName);		
                       } else {
			  		      failedTests.add(testName);
				      }
				
 			      }
                  conn.disconnect();
			   }
			}

			if (passedTests.size() > 0) {
				System.out.println("Passed Tests:");
				for (int i=0; i <= passedTests.size() - 1; i++){
				   System.out.println(passedTests.get(i));
			    }
			}
			if (failedTests.size() > 0) {
			   System.out.println("Failed Tests:");
			   for (int i=0; i <= failedTests.size() - 1; i++){
				   System.out.println(failedTests.get(i));
			   }
			}
        } catch (Exception e) {
            // Something is wrong.
            e.printStackTrace();
        }
    }

}


