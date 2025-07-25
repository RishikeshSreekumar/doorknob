# Insta-clone

This is a simple Instagram clone application with a Next.js frontend and a FastAPI backend.

## Prerequisites

- Docker
- Docker Compose

## Running the application

1.  Clone the repository.
2.  Open a terminal and navigate to the root of the project.
3.  Run the following command:

    ```bash
    docker-compose up --build
    ```

4.  The frontend will be available at `http://localhost:3000` and the backend at `http://localhost:8000`.

## Project Structure

-   `frontend/`: Contains the Next.js application.
-   `backend/`: Contains the FastAPI application.
-   `docker-compose.yml`: Defines the services for the application.

## API Endpoints

-   `POST /posts/`: Create a new post.
    -   **Form data:**
        -   `text`: The text of the post.
        -   `image`: The image file for the post.
-   `GET /posts/`: Get all posts.
