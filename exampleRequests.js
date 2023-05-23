/*
    Here's a few fetch request examples from https://docs.dashboard.getawair.com/
    in Javascript using the Fetch API. 

    The optional parameters in the fetch URLs include:
    * from: Start of time range. If time range given is greater than maximum range (1 hour), 
            then only 1 hour will be returned, and the rest will need to be made in separate 
            calls with your own pagination method. Default is 1 hour before current time.
    * to: End of time range. Default is current time.
    * limit: Number of AirData points returned from the supplied time range. Maximum: ~360
    * desc: Return AirData in descending order before to (true) or after from (false) datetime. 
            Default of true returns AirData descending from the to parameter (Current DateTime, 
            if to is not supplied). (boolean)
    * fahrenheit: Return temperature in Fahrenheit (boolean)
*/

var deviceID = "28563"; //"17987"
var orgID = "10994";
var apiKey = "UfwaYhhnQJDJ1GoX37GHDy6CmPstQGyl";

var from = new Date('13 April 2023 14:15');
var to = new Date('13 April 2023 14:25');

var myHeaders = new Headers();
myHeaders.append("x-api-key", apiKey);
var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow',
  };

/* Fetch all data for all measurements in the time interval. */
fetch('https://developer-apis.awair.is/v1/orgs/' + orgID + '/devices/awair-omni/' + deviceID + '/air-data/raw?from=' + from.toISOString() + '&to=' + to.toISOString() + '&limit=360&desc=false&fahrenheit=false', requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

/* Fetch the 5-minute interval averages for all measurements in the time interval. */
fetch('https://developer-apis.awair.is/v1/orgs/' + orgID + '/devices/awair-omni/' + deviceID + '/air-data/5-min-avg?from=' + from.toISOString() + '&to=' + to.toISOString(), requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

/* Fetch the 15-minute interval averages for all measurements in the time interval. */
fetch('https://developer-apis.awair.is/v1/orgs/' + orgID + '/devices/awair-omni/' + deviceID + '/air-data/15-min-avg?from=' + from.toISOString() + '&to=' + to.toISOString() + '&limit=100&desc=true&fahrenheit=false', requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

/* View your device's time zone. */
fetch('https://developer-apis.awair.is/v1/orgs/' + orgID + '/devices/awair-omni/' + deviceID + '/timezone', requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

/* View all devices and their locations. */
fetch('https://developer-apis.awair.is/v1/orgs/' + orgID + '/devices', requestOptions)
.then(response => response.text())
.then(result => console.log(result))
.catch(error => console.log('error', error));
