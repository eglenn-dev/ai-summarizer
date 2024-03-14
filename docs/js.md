# JavaScript Files Functionality Documentation

This markdown file documents the functionality of the three JavaScript files in the Python AI Tools project:

## gemini-api.js

This file provides a common interface for interacting with the Gemini AI models through the Python backend.

### Key Functionalities:

-   `streamGemini` function:

    -   Takes parameters like model name, stream URL, URL to summarize, and form data.
    -   Sends a POST request to the specified stream URL with the provided data.
    -   Uses the `streamResponseChunks` function to handle the response stream.

-   `streamResponseChunks` function:
    -   Processes the response stream from the backend.
    -   Extracts text chunks and handles errors.
    -   Yields text chunks to the caller.

## site.js

This file handles the website summarization functionality on the `/site` page.

### Key Functionalities:

-   Form submission handler:
    -   Prevents default form submission behavior.
    -   Extracts the URL from the input field.
    -   Calls the `streamGemini` function to generate a summary.
    -   Updates the output element with the received summary chunks.
    -   Handles errors and displays them in the output element.

## upload.js

This file handles the document summarization functionality on the `/doc` page.

### Key Functionalities:

-   Form submission handler:
    -   Prevents default form submission behavior.
    -   Extracts the uploaded PDF file.
    -   Creates a FormData object and appends the file.
    -   Calls the `streamGemini` function to generate summaries, sentiment analysis, and questions.
    -   Updates the output element with the received text chunks, formatted as markdown.
    -   Handles errors and displays them in the output element.

## Commonalities:

Both `site.js` and `upload.js` share the following functionalities:

-   Use the `streamGemini` function to interact with the AI models.
-   Update the output element with the received text chunks.
-   Handle errors and display them appropriately.

## Notes:

-   The JavaScript files rely on the `markdown-it` library for markdown formatting.
-   The `base64-js` library is used for handling base64 encoding/decoding.
-   Error handling is implemented to provide feedback to the user in case of issues.
