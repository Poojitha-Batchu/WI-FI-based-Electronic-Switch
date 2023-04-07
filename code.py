
/*The network library allows us to connect the ESP32 to a Wi-Fi network.
We need to import the Pin class from the machine module to be able to interact with the GPIOs. */
import network
from machine import Pin 


/*  we create our web server using sockets and the Python socket API. 
The official documentation imports the socket library as follows:*/
try:
  	import usocket as socket
except:
  	import socket


def wlan_connect(ssid,pwd):
	//set the ESP32 as a Wi-Fi station
   	 wlan = network.WLAN(network.STA_IF)              
  	  if not wlan.active() or not wlan.isconnected():
 		//activate the station  
      		  wlan.active(True)             
	          // the ESP32 connects to your router using the SSID and password defined                                   
      		  wlan.connect(ssid,pwd)                                 	   
	  //The following statement ensures that the code doesn’t proceed while the ESP is not connected to your network.
           while not wlan.isconnected():
           	 pass
	   /*After a successful connection, print network interface parameters like 
           the ESP32 IP address – use the ifconfig() method on the wlan object. */
           print('network config:', wlan.ifconfig())
wlan_connect('Bunny', 'qwertyui')


//Create a Pin object called led that is an output, that refers to the ESP32 GPIO2 and GPIO5
led1 = Pin(2, Pin.OUT)
led2 = Pin(5, Pin.OUT)


/* The script starts by creating a function called web_page().
 This function returns a variable called html that contains the HTML text to build the web page.*/
def web_page():
	 //The web page displays the current GPIO state. So, before generating the HTML text, we need to check the LED state.
	 We save its state on the gpio_state variable:
 	 if led1.value() == 1:
   		 gpio_state1 = "ON"
 	 else:
 		  gpio_state1 = "OFF"
    
	  if led2.value() == 1:
  		  gpio_state2 = "ON"
 	 else:
  		  gpio_state2 = "OFF"  
  

//After that, the gpio_state variable is incorporated into the HTML text using “+” signs to concatenate strings.
  html = """<html><head> <title>Wi-fi based Electronic Switch</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #87EE68; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #F7314C;}</style></head><body> <h1>ESP Web Server</h1> 
  <p>Bulb-1 state: <strong>""" + gpio_state1 + """</strong></p><p><a href="/?led1=on"><button class="button">ON</button></a></p>
  <p><a href="/?led1=off"><button class="button button2">OFF</button></a></p>
  <p>Bulb-2 state: <strong>""" + gpio_state2 + """</strong></p><p><a href="/?led2=on"><button class="button">ON</button></a></p>
  <p><a href="/?led2=off"><button class="button button2">OFF</button></a></p>
  </body></html>"""
  return html


/*Create a socket using socket.socket(), and specify the socket type. We create a new socket object called s with the 
given address family, and socket type. This is a STREAM TCP socket*/
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

/*Next, bind the socket to an address (network interface and port number) using the bind() method. 
The bind() method accepts a tupple variable with the ip address, and port number 
we are passing an empty string ‘ ‘ as an IP address and port 80. In this case, the empty string refers to the localhost IP address (this means the ESP32 IP address).*/
s.bind(('', 80))

/* The next line enables the server to accept connections; it makes a “listening” socket. The argument 
specifies the maximum number of queued connections. The maximum is 5.*/
s.listen(5)

/* In the while loop is where we listen for requests and send responses.
 When a client connects, the server calls the accept() method to accept the connection.
 When a client connects, it saves a new socket object to accept and send data on the conn variable, and
 saves the client address to connect to the server on the addr variable.*/

while True:
 	 conn, addr = s.accept()
	// print the address of the client saved on the addr variable.
  	print('Got a connection from %s' % str(addr))
	/*The data is exchanged between the client and server using the send() and recv() methods.
	The following line gets the request received on the newly created socket and saves it in the request variable
	The recv() method receives the data from the client socket (remember that we’ve created a new socket object on the conn variable). 
	The argument of the recv() method specifies the maximum data that can be received at once.*/
  	request = conn.recv(1024)
 	request = str(request)
	//prints the content of the request
  	print('Content = %s' % request)
  
  	led1_on = request.find('/?led1=on')
  	led1_off = request.find('/?led1=off')
  	if led1_on == 6:
    		print('LED1 ON')
    		led1.value(1)
  	if led1_off == 6:
    		print('LED1 OFF')
    		led1.value(0)
    
  	led2_on = request.find('/?led2=on')
  	led2_off = request.find('/?led2=off')
  	if led2_on == 6:
    		print('LED2 ON')
    		led2.value(1)
  	if led2_off == 6:
    		print('LED2 OFF')
    		led2.value(0)

  //create a variable called response that contains the HTML text returned by the web_page() function  
  response = web_page()


//Finally, send the response to the socket client using the send() and sendall() methods
//In the end, close the created socket.
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close
