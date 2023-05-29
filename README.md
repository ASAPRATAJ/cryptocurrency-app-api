# Cryptocurrency App API

* The Cryptocurrency App API is a RESTful API designed for voting on selected cryptocurrencies obtained from the 
CoinGecko website. 
* It allows users to vote for their preferred cryptocurrencies and provides features to track the 
cryptocurrency with the highest percentage change based on the votes received. 
* Every user has 3 votes.
* User can vote only on the first day of the month.
* The votes are counted on the last day of 
each month.
* Users who have voted for the winning cryptocurrency are awarded with the "gem_finder" badge in their profile.


The application is containerized using Docker and utilizes PostgreSQL as the database. 
The following technologies are used in the development of this API:

* Django
* Django REST Framework
* Django corsheaders (for controlling access to Django REST API from other domains or origins)
* Celery (for scheduling tasks)
* Docker
* PostgreSQL
* Psycopg2: (Python library for connecting to PostgreSQL databases)
* Swagger (for OpenAPI schema)
* CoinGecko API (for obtaining cryptocurrency data)


## Endpoints:

### Coin:

* __GET ' /api/coin/list/ '__ : Retrieves a list of cryptocurrencies from CoinGecko.

### User

* __POST ' /api/user/create/ '__ : Allows creating a new user.
* __GET ' /api/user/me/ '__ : Displays information about the currently logged-in user.
* __PUT ' /api/user/me/ '__ : Allows updating information in the user's profile.
* __PATCH ' /api/user/me/ '__ : Allows partial updates to the user's profile information.
* __POST ' /api/user/token/ '__ : Generates a token that provides authentication credentials for the logged-in user.

### Vote

* __GET ' /api/vote/votes/ '__ : Retrieves a list of cast votes.
* __POST ' /api/vote/votes/ '__ : Allows casting a vote for a chosen cryptocurrency, associating it with the logged-in 
user and 
the current price of the cryptocurrency.
* __GET ' /api/vote/votes/{id}/ '__ : Retrieves details about a specific vote, including the justification for voting 
for a particular cryptocurrency.
* __PUT/PATCH/DELETE ' /api/vote/votes/{id}/ '__ : Requests allowed only for users with superuser privileges.

Please refer to the API documentation or the Swagger UI for more details on the request and response formats for 
each endpoint.

## Getting Started

To run the API locally, follow these steps:

1. Clone the repository.
2. Set up the PostgreSQL database and configure the database settings.
3. Build and run the Docker containers.
4. Access the API endpoints using a tool like Postman or a web browser. 
The API endpoints will be available at http://localhost:8000/. You can send requests to this address to interact with the API.


## Contributing

Contributions to improve and enhance the API are welcome. 
If you encounter any issues or have suggestions for new features, please submit an issue or create a pull request.

## License

This API is released under the Open Source License. 

## Contact

If you have any questions or need further assistance, please contact the project maintainer with email: 
__bartosz.ratajewski@gmail.com__



Enjoy using the Cryptocurrency App API!
