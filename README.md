# BriteCoreAPI
A risk API developed for the wonderful folks at BriteCore

Greetings BriteCore!

It is here that I am happy to present the flexible risk API detailed in the demo project that I was asked 
to create. For deployment I used a MySQL database hosted through Amazon Web Services (AWS) Relational Database 
Service. I used Python combined with Pony to generate ORMs and map to the tables in the database with 
PyMySQL connecting to the database itself.

The ORMs are as follows:

class Risk(db.Entity):
    r_id = PrimaryKey(int, auto=True)
    r_name = Required(str, unique=True)
    field = Set("Field")
class Field(db.Entity):
    f_id = PrimaryKey(int, auto=True)
    f_name = Required(str)
    f_type = Required(str)
    f_r_id = Required(Risk)
    enum = Set("Enum")
class Enum(db.Entity):
    e_id = PrimaryKey(int, auto=True)
    e_name = Required(str)
    e_f_id = Required(Field)
 
I created a group of four functions utilizing Pony’s framework to query the database.
The first, risk query, grabs all of the related information for a risk passed as a parameter
and puts all of the information into a dictionary so the information is JSON compatible and is 
ready to be passed through the API.  I then created an all risks function that uses risk 
query to get the information of all risks in the database and wraps it in a dictionary to be 
handed to an API endpoint.  Single risk is a function that grabs a risk specified as a parameter 
and uses the risk query function to get the associated information and then wraps the data in a 
dictionary to maintain the same structure as the all risks function.  The final function is 
only risks which just grabs a list of just the risk names and identifiers for a drop-down 
selection on the HTML page.

I then used Flask, Flask-Restful, and Flask_CORS to handle API creation and permissions.
I created three API endpoints.  One to grab all risks and their associated information, a 
similar endpoint to do the same for a single risk, and a third for just obtaining the risk 
names and IDs.  I packaged the python file using Zappa and uploaded it to a Lambda function 
on AWS where the API is readily available through the AWS API Gateway that Zappa automatically created.

From there I created a simple HTML page that utilizes Vue.js to dynamically populate a form 
based on the fields associated with selected risks.  A risk is selected by either picking a 
risk from a drop-down list, or selecting to view all risks at once.  These functions call the 
created API endpoints to determine what fields are then shown on the form.  The fields have 
appropriate input fields created dynamically, with date-pickers for dates, drop-down selections 
for enums, numerical fields for numbers, and text fields for text.  When a risk or all risks are 
selected a submit button is also shown dynamically though it has limited functionality as per the 
scope of the project.

The HTML file and associated Javascipt file were uploaded to an S3 AWS bucket and hosted live from 
there.  You can see a live instance of the whole project working together here.

The above describes the functionality of the final product, but I thought it might be of interest to 
know the process I used to create it.  I first developed the entire project locally starting with an 
SQLite database and running an instance of the API with the HTML page on my local machine.  I then began 
hosting components of the project progressively on AWS starting with the backend and continuing until the 
full stack was hosted online.  Below is a list of all of the languages, packages, and tools used to create 
this project and I would proudly like to share that prior to this project I only had passing experience with 
Python and limited experience with JavaScript.  I look forward to learning and mastering new tools and projects 
in the future!

Thank you for the opportunity,
Oliver Thompson


Tools Utilized:
AWS: Lambda, API Gateway, S3, CloudFormation, RDS
Vue.js
Zappa
VirtualEnv
Flask_CORS
Flask-Restful
Flask
Python 2.7
Pony
PyMySQL
MySQL
SQLite
