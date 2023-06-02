# Awair
Collect data from an Awair Omni device

 From dashboard.awair.com, you can export air quality data for any time window at 5-minute intervals.  Select Awair Dashboard > Export Data, select your time interval, 
 and download a .zip file with your data as a CSV.    
    
 If you need to extract data at intervals other than 5 minutes (as short as 10 seconds), there are two options:
 
 (1) Use awair_collectData.js. Follow the usage instructions at the top of the file. This script saves a single CSV file with data from any time window at intervals 
    as short as 10 seconds. 
      Note: To prevent denial of servie (DOS) attacks, Awair sets a limit on the number of data entries you can extract in 1 minute. Therefore, this script pauses for 
        60 seconds after collecting 10 hours' worth of data, so extracting many days' worth of data can take several minutes.
      
 (2) Write your own script using examples from exampleRequests.js or https://docs.dashboard.getawair.com/. Note that the first example in this file only allows you 
      to fetch 1 hour's worth of data. To export data for a longer time window, use awair_collectData.js.
      
 Contact the UA Sensor Lab with any questions. If you borrowed our Awair device, contact us to get the DeviceID, OrgID, and API Key.
 
