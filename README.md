# Django School Management System
This an open source school management system API built with Django and Django-rest framework for managing school or college. It provides an API for administration, admission, attendance, schedule and results. It also provide users with different permissions to access various apps depending on their access level.

Techdometz is a tech startup helping schools and education centers to provide solutions to their tech problems. 
[Contact us](http://techdometz.com/contact-us/) for details.

# Quick Install
You should have at least basic django and django-rest framework experience to run django-scms. We test only in PostgreSQL database.

### Fork the repo
You first need to fork the repo from [Techdometz](https://github.com/TechDometz/django-scms).
### Clone the repo
Clone the forked repo

`git clone https://github.com/[username]/django-scms.git`  

### Create a virtual environment

There are several ways depending on the OS and package you choose. Here's my favorite  
`sudo apt-get install python3-pip`  
`pip3 install virtualenv`  
Then either  
`python3 -m venv venv`  
or  
`python -m venv venv`  
or  
`virtualenv venv` (you can call it venv or anything you like)

#### Activate the virtual environment  

in Mac or Linux
`source venv/bin/activate`  
in windows
`venv/Scripts/activate.bat`  

# Apps

##School Information System (SIS)
This tracks the students’ information and their parent/guardian/contact information. This module also records, basic classes information, and school year information. This is the central module for django-scms and is required for use of any other module. All other modules are optional.

##Admissions
This tracks potential students and their registration processes. It allows various admission levels to be added as well as steps that need to be completed before moving onto the next level. It also tracks any open houses a student has attended and how the student heard about the school.

## Contributors

- [Mwinamijr](https://github.com/mwinamijr)

## License

The project is licensed under the MIT License
