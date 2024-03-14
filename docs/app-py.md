# Functionality Documentation: app.py

This markdown file documents the functionality of the app.py file in the Python AI Tools project.

## Overview

The app.py file serves as the main entry point for the Flask application. It handles routing, request processing, and interaction with the AI summarization models.

## Key Functionalities:

### 1. Flask App Initialization:

-   Creates a Flask application instance.
-   Configures the upload folder and allowed file extensions for document summarization.

### 2. Route Definitions:

-   Defines routes for various pages and API endpoints:
    -   `/`: Serves the main page.
    -   /site: Serves the website summarization page.
    -   /doc: Serves the document summarization page.
    -   /api: Redirects to the main page.
    -   /api/site: Processes website summarization requests.
    -   /api/doc: Handles document summarization requests.

### 3. API Endpoints:

-   /api/site:
    -   Accepts POST requests with a JSON body containing the URL and desired model.
    -   Uses the website_parser module to extract text from the website.
    -   Calls the specified AI model to generate a summary.
    -   Streams the summary back to the client as a text event stream.
-   /api/doc:
    -   Accepts POST requests with an uploaded PDF file.
    -   Extracts text from the PDF using PyPDF2.
    -   Calls the AI model to generate a summary, sentiment analysis, and questions.
    -   Streams the results back to the client as a text event stream.
-   Helper Functions:
    -   allowed_file: Checks if an uploaded file has an allowed extension.
    -   make_document: Creates a new PDF document with the generated summaries and merges it with the original document.
    -   calculate_bullet_points: Calculates the desired number of bullet points for the summary based on document length.
    -   count_pages: Counts the number of pages in a PDF document.

## Dependencies:

The app.py file relies on various libraries and modules, including: - Flask - google-generativeai - website_parser - PyPDF2 - reportlab - markdown

## Notes:

-   The API key for accessing the AI models is stored in the .env file.
-   The application uses markdown formatting for displaying summaries.
-   Error handling is implemented to catch exceptions and return appropriate responses.
