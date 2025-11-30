# Task CRUD API — Endpoints & Validation (v1)

## POST /tasks
Create a new task. Validates all fields.

**Request Body Example**
{
"userId": 1,
"category": "school",
"colorShade": 3,
"title": "Submit final essay",
"description": "Research and submit by Friday.",
"dueDate": "2024-06-14",
"doDate": "2024-06-12",
"url": "https://canvas.edu/submissions/123",
"orderIndex": 1
}


**Validation Rules:**
- `title`: required, must not be empty
- `dueDate`/`doDate`: required, must be valid format (YYYY-MM-DD)
- `colorShade`: integer, must be in allowed range (e.g. 0–5)
- All fields required unless specified

**Success Response:** `201 Created` — Returns created task object.
**Error Response:** `400 Bad Request` — Error message describing the issue.

---

## GET /tasks?userId=<userId>
Fetch all tasks for a user, sorted by `orderIndex` ascending.

**Response:** Array of task objects.

---

## PUT /tasks/{taskId}
Update an existing task. Same body and validations as POST.

**Success Response:** `200 OK` with updated task object.
**Error Response:** `400 Bad Request` — Error message.

---

## DELETE /tasks/{taskId}
Delete the specified task.

**Success Response:** `204 No Content`
**Error Response:** `404 Not Found` if `taskId` invalid.

---

## Drag-and-Drop Ordering
To reorder tasks, update the `orderIndex` field for changed tasks using the `PUT` endpoint.

---

## Error Responses
All errors return a JSON object:
{ "error": "Validation failed: title is empty." }

