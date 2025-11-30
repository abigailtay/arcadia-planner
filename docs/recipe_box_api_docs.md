# Recipe Box API Documentation

## Overview

The Recipe Box API supports full CRUD operations on recipes, filtering by categories and subcategories, sticker assignment, and fractional measurement handling.

---

## API Endpoints

### 1. Create Recipe

- **URL:** `/recipes`
- **Method:** POST
- **Content-Type:** application/json
- **Request Body Fields:**
  - `"title"`: string (required)  
  - `"instructions"`: string (optional)  
  - `"categoryId"`: integer (optional)  
  - `"subcategoryId"`: integer (optional)  
  - `"stickerId"`: integer (optional)  
  - `"measurement"`: string representing fraction format, e.g., `"1/2"` (optional)

- **Response:**
  - Status Code: 201 Created
  - Body:
    ```
    {
      "success": true,
      "recipeId": 123
    }
    ```

- **Errors:**
  - 400 Bad Request if `title` missing or measurement malformed.

---

### 2. Update Recipe

- **URL:** `/recipes/<recipeId>`
- **Method:** PUT
- **Content-Type:** application/json
- **Request Body Fields:** Any subset of creation fields (`title`, `instructions`, `categoryId`, `subcategoryId`, `stickerId`, `measurement`)
- **Response:**
  - Status Code: 200 OK
  - Body:
    ```
    {
      "success": true
    }
    ```
- **Errors:**
  - 400 Bad Request on invalid inputs.
  - 404 Not Found if recipeId does not exist.

---

### 3. View Recipe

- **URL:** `/recipes/<recipeId>`
- **Method:** GET
- **Response:**
  - Status Code: 200 OK
  - Body:
    ```
    {
      "success": true,
      "recipe": {
        "recipeId": 123,
        "title": "Apple Pie",
        "instructions": "...",
        "categoryId": 1,
        "subcategoryId": 2,
        "stickerId": 5,
        "measurement": "3/4"    // fraction formatted string from internal decimal
      }
    }
    ```
  - 404 Not Found if recipe not found

---

### 4. Filter Recipes

- **URL:** `/recipes`
- **Method:** GET
- **Query Parameters (optional):**
  - `categoryId`: integer
  - `subcategoryId`: integer

- **Response:**
  - Status Code: 200 OK
  - Body:
    ```
    {
      "success": true,
      "recipes": [
        {
          "recipeId": 123,
          "title": "Apple Pie",
          "categoryId": 1,
          "subcategoryId": 2,
          "stickerId": 5,
          "measurement": "3/4"
        },
        ...
      ]
    }
    ```

---

### 5. Delete Recipe

- **URL:** `/recipes/<recipeId>`
- **Method:** DELETE
- **Response:**
  - Status Code: 200 OK
  - Body:
    ```
    {
      "success": true
    }
    ```

---

### 6. Create Sticker

- **URL:** `/stickers`
- **Method:** POST
- **Content-Type:** application/json
- **Request Body Fields:**
  - `"name"`: string (required) - Sticker label
  - `"imageURL"`: string (required) - URL to sticker image/icon

- **Response:**
  - Status Code: 201 Created
  - Body:
    ```
    {
      "success": true,
      "stickerId": 5
    }
    ```

- **Errors:**
  - 400 Bad Request if missing fields or invalid URL format.

---

## Notes on Fractional Measurement

- Measurements are stored internally as decimals (floats) but exposed externally as simplified fractions for user readability.
- Front end should send fractional strings like `"1/2"`, `"3/4"`, and backend will convert them for storage.
- API responses will return fractions as strings.

---

## Front End Integration Notes

- Front end must provide the sticker imageURL when creating stickers.
- Stickers must be created before they can be assigned to recipes.
- All field names and types must match exactly the above contract.
- Proper error handling is mandatory for bad input or missing fields.

---