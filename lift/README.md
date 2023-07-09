Elevator System README

This README document outlines the thought process, design decisions, and instructions for setting up and testing the Elevator System API developed using Django and Django REST Framework.

Thought Process
The Elevator System is a simplified model that emulates an elevator system with the ability to make request for elevator to the given floor to the desired floor, it also shows a list of requests to the particular elavator

Design Decisions
Architecture
The Elevator System is built using Django and Django REST Framework, which provides a robust and scalable framework for building APIs. The application follows the Model-View-Controller (MVC) architecture pattern.

Repository File Structure
The project is organized into several directories:

lift/- This directory contains the settings and configuration files for the Django project.
liftapi/ - This directory contains the models, serializers, and viewsets for the Elevator API.

Database Modelling
The Elevator System uses SQLite Database with 3 models: Elevator, ElevatorSystem and ElevatorRequest.


The following libraries are used in the Elevator System:

Django: A high-level Python web framework that enables rapid development of secure and maintainable websites and APIs. / Django REST Framework: A powerful and flexible toolkit for building APIs that includes serializers, viewsets, and authentication support. /

1. for getting info of elevator system by elevatorSystem name
'elevator-systems/<str:system_name>/'

2. for checking status of particular elevator
'elevator-systems/<int:elevator_system>/elevators/<int:pk>/status/'

3. for patch request for update elaevator details
'elevator-systems/<int:elevator_system>/elevators/<int:pk>/'

4. get list of all the request of paricular elevator
'elevator-systems/<int:elevator_system>/elevators/<int:pk>/requests/'

5. to make a request of elevator from current floor to desired floor
'elevator-systems/<int:pk>/create-elevator-request',

6. along with all the routers default urls
    ('', include(router.urls)),


Test
To test the application, you can follow these steps:

Activate the virtual environment: source env/scripts/activate
install python, django, and django rest framework
Verify that the responses are correct and the application is functioning as expected.
Conclusion
