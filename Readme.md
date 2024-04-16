# Social Networking Application API Documentation

## Description

The Social Networking Application API is designed to facilitate social interactions between users. It provides features such as user authentication, friend requests, user profiles, and user search. Users can sign up for an account, log in securely, search for other users, send friend requests, and manage their list of friends.

## Installation

### Using Docker

1. Clone the repository:
    ```bash
    git clone 
    ```
2. Navigate to the project directory:
    ```bash
    cd Accuknox_Task
    ```
3. Build the Docker image:
    ```bash
    docker-compose build
    ```
4. Start the Docker containers:
    ```bash
    docker-compose up
    ```
5. Access the application at `http://localhost:8000`
6. Postman Collection: [Social Networking API](https://www.postman.com/technical-engineer-61904315/workspace/accuknox/collection/33[…]0ea-7909-4d03-93ac-b4562546b95b?action=share&creator=33267109)

## API Documentation

### User Authentication

#### User Signup

- **Create User**
  - Method: POST
  - URL: `/signup/`
  - Authentication: Basic
  - Request Body:
    ```json
    {
        "email": "root@gmail.com",
        "password": "root",
        "name":"root",
        "Gender":"Male",
        "phonenumber":1234567894,
    }
    ```
  - Response: JSON object indicating success or failure.

#### User Login

- **User Login**
  - Method: POST
  - URL: `/login/`
  - Authentication: Basic
  - Request Body:
    ```json
    {
        "email": "root@gmail.com",
        "password": "root"
    }
    ```
  - Response: JSON object indicating success or failure.


### User Search

- **Search Users**
  - Method: GET
  - URL: `/search/`
  - Authentication: Basic
  - Query Parameters:
    - `search` (required): The search query to find users by email or username.
  - Response: JSON array containing users matching the search query.
  - Example Response Body:
    ```json
    {
        "count": 5,
        "next": null,
        "previous": null,
        "results": [
            {
                "email": "user1@example.com",
                "name":"user1",
            },
            {
                "email": "user2@example.com",
                "name":"user2",
            },
            {
                "email": "user3@example.com",
                "name":"user3",
            }
        ]
    }

### Friend Requests

#### Create Friend Request

- **Send Friend Request**
  - Method: POST
  - URL: `/friend-request/`
  - Authentication: Basic
  - Request Body:
    ```json
    {
        "to_user": "friend@example.com"
    }
    ```
  - Response: JSON object indicating success or failure.

#### Accept Friend Request

- **Accept Friend Request**
  - Method: POST
  - URL: `/friends/`
  - Authentication: Basic
  - Response: JSON object indicating success or failure.

#### List Pending Requests

- **List Pending Requests**
  - Method: GET
  - URL: `/pending-requests/`
  - Authentication: Basic
  - Response: JSON array containing pending friend requests.

#### Reject Friend Request

- **Reject Friend Request**
  - Method: POST
  - URL: `reject-request/<int:pk>/`
  - Authentication: Basic
  - Response: JSON object indicating success or failure.

    ```

#### Accept Friend Request

- **Accept Friend Request**
  - Method: POST
  - URL: `/accept-friend-request/<int:request_id>/`
  - Authentication: Basic
  - Response: JSON object indicating success or failure.

### Pagination

- **Add Pagination to User Search**
  - Method: GET
  - URL: `/search/?q=johndoe&page_size=20`
  - Authentication: Basic
  - Query Parameters:
    - `q` (required): The search query.
    - `page_size`: The number of results per page.
  - Response: JSON array containing paginated user search results.

## Usage

Follow the API documentation to interact with the Social Networking Application API. Ensure that you have valid authentication credentials for accessing protected endpoints.
