This application is build over StackOverflowAPI for searching questions in StackOverflow

How to use:

- Run below commands in terminal one by one

	-/stackoverflowAPI_implementation$ source env/bin/activate
	
	-(env) /stackoverflowAPI_implementation/stackoverflow_project$ python manage.py runserver

- Browse to localhost url - http://127.0.0.1:8000/search/
- This is 'POST' api call
- need to provide content in below format
		{
		  "user_id" : "2",
		  "tagged": "django",
		  "nottaged": "java",
		  "intitle" : "django",
		  "order" : "asc",
		  "sort" : "activity",
		  "pagesize" : "30",
		  "page" : "1",
		  "fromdate" : "2021/05/12",
		  "todate" : "2021/06/12"
		}
		
	Constraints:
	
	-'user_id' field is complusory	
	-'tagged' and 'intitle' cannot be None at sametime	
	-'nottagged' can only be used if tagged is used	
	-acceptable value for sort can only be one of - ['activity', 'creation', 'votes', 'relevance']	
	-acceptable value for order can only be one of - ['desc', 'asc']

Constraints:
- Only 5 searches per minute are allowed
- Only 100 searches per day are allowed

Note:Caching is implemented in this application, if the application is restarted all the caching data will be lost

Database used - MYSQL

