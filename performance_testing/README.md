# How to do performance tests

1. Load the performance test you want to use in jmeter
2. Edit the url variable to point to the url that you want to test  
2.1  You will likely need to be on the same subnet as the app that you test. Do not run the jmeter test on the same machine running the app. 
3. Save the file
4. Run jmeter on your test machine (again, different hardware from the machine running the app) with the following command: 
```
./jmeter.sh -n -t /path/to/test_plan.jmx -l ~/path/to/test_results.jtl
```
Do not use the jmeter GUI, it slows down the test and adds noise to the results. 

# How to glean data from the performance tests: 
1. Open jmeter
2. navigate to:  tools -> generate html report -> select test_results.jtl
3. Use your browser to look at all the pretty charts and statistics!
