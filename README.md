What your application does
- The application uses fastAPI to predict housing prices for California. 

How to build your application
- The app was built using docker.

How to run your application
- The run.sh file includes all steps necessary to run the app

How to test your application
- Pytest was used to implement unit-testing. The run.sh script has further details on how to test each endpoint.



What does Pydantic handle for us?
- Pydantic is a useful library for data validation and handling common data errors.

What do GitHub Actions do?
- Github actions allows us to automate the build, test, and deployment pipeline in a CI/CD fashion.

In 2-3 sentences (plain language), describe what the Sequence Diagram below shows.
- The sequence diagram shows the workflow of the app. The user makes a POST call to provide the app with the necessary features required to predict the house price. The API uses pydantic to test for correct values and returns the user the output, i.e, the price of the house.