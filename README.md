# Audio-server-api
`Audio-server-api` is a Flask web API that simulates the behavior of an audio file 
server while using a SQL database.

## Production environment:
The app is deployed on Heroku and can be tested using Postman or any other API testing tool. If you are testing using Postman, please feel free to download the `Audio Server API Test.postman_collection.json` [Exported as Collection v2.1] file and import it in Postman.
### App url: https://audioapi.herokuapp.com

## Usage:
To setup and use the api on your local device, follow the instructions:

### Setting up the environment:
To setup the environment with the packages needed to run the app, first create a virtual environment and then install the packages from the `requirements.txt`

```
>> conda create --name myenv python=3.8
>> pip install -r requirements.txt
```

## Supported files and their fields
The API supports 3 audio file types (`audioFileType`), they are:
1. `song`
2. `podcast`
3. `audiobook`

### Song file fields:
- `id`: Unique identifier set automatically
- `name`: Name of the song, passed in request body – (mandatory, string, cannot be larger than 100 characters)
- `duration`: Duration in number of seconds, passed in request body – (mandatory, integer, positive)
- `uploaded_time` Uploaded time, set automatically to the time when a record gets saved in the database

### Podcast file fields:
- `id`: Unique identifier set automatically
- `name`: Name of the song, passed in request body – (mandatory, string, cannot be larger than 100 characters)
- `duration`: Duration in number of seconds, passed in request body – (mandatory, integer, positive)
- `host`: Host of the podcast, passed in request body – (mandatory, string, cannot be larger than 100 characters)
-  `participants`: Participants, passed in request body as a list of strings (optional, list of strings, each string cannot be larger than 100 characters, maximum of 10 participants possible)
- `uploaded_time` Uploaded time, set automatically to the time when a record gets saved in the database


### AudioBook file fields:
- `id`: Unique identifier set automatically
- `name`: Name of the song, passed in request body – (mandatory, string, cannot be larger than 100 characters)
- `duration`: Duration in number of seconds, passed in request body – (mandatory, integer, positive)
- `author`: Author of the song, passed in request body – (mandatory, string, cannot be larger than 100 characters)
- `narrator`: Narrator of the song, passed in request body – (mandatory, string, cannot be larger than 100 characters)
- `uploaded_time` Uploaded time, set automatically to the time when a record gets saved in the database


## API endpoints and how to use them:

The api mainly have 3 endpoints, they are:
1. `{{url}}/{{audioFileType}}` -> Get list of all records available
2. `{{url}}/{{audioFileType}}/{{audioFileID}}` -> Get, update or delete a specific file
3. `{{url}}/` -> create a new file

### Create a Song:
Endpoint: `{{url}}/`
Request Body:
```json
{
    "audioFileType": "song",
    "audioFileMetadata": {
        "name": "Test",
        "duration": 360
    }
}
```

Resonse status code: 200
Sample Response data if song is successfully created:
```json
{
    "id": 30,
    "name": "Test",
    "duration": 360,
    "uploaded_time": "2021-03-21T13:15:38.612827"
}
```

if there was a problem in creating a record, 400 status code will be returned.
#### Conditions to keep in mind:
- name, duration, host is mandatory fields


### Create a Podcast:
Endpoint: `{{url}}/`
Request Body:
```json
{
    "audioFileType": "podcast",
    "audioFileMetadata": {
        "name": "Test podcast",
        "duration": 360,
        "host": "Test host",
        "participants": [
            "participant 1",
            "participant 2",
            "participant 3"
        ]
    }
}
```

Resonse status code: 200
Sample Response data if song is successfully created:
```json
{
    "id": 31,
    "name": "Test podcast",
    "duration": 360,
    "host": "Test host",
    "participants": [
        "participant 2",
        "participant 1",
        "participant 3"
    ],
    "uploaded_time": "2021-03-21T13:22:05.923891"
}
```

if there was a problem in creating a record, 400 status code will be returned.
#### Conditions to keep in mind:
- name, duration, host is mandatory fields
- participants list is optional
- participants cannot have more than 10 participants

If any of these conditions are not satisfied in the request body, record will not be created and 400 status code will be returned along with the specific validation error.

### Create a AudioBook:
Endpoint: `{{url}}/`
Request Body:
```json
{
    "audioFileType": "audiobook",
    "audioFileMetadata": {
        "name": "Test audiobook",
        "duration": 3600,
        "author": "Test author",
        "narrator": "Test narrator"
    }
}
```

Resonse status code: 200
Sample Response data if song is successfully created:
```json
{
    "id": 32,
    "name": "Test audiobook",
    "duration": 3600,
    "author": "Test author",
    "narrator": "Test narrator",
    "uploaded_time": "2021-03-21T13:27:31.020855"
}
```

if there was a problem in creating a record, 400 status code will be returned.
#### Conditions to keep in mind:
- name, duration, author, narrator are mandatory fields

If any of these conditions are not satisfied in the request body, record will not be created and 400 status code will be returned along with the specific validation error.

## Get/DELETE a Specific record:
Endpoint: `{{url}}/{{audioFileType}}/{{audioFileID}}`

### GET:
Example GET request: `{{url}}/song/30`

Example Response (200 OK):
```json
{
    "id": 30,
    "name": "Test",
    "duration": 360,
    "uploaded_time": "2021-03-21T13:15:38.612827"
}
```
### DELETE:
Example DELETE request: `{{url}}/song/30`

Example Response (200 OK):
```json
{
    "Message": "Successfully deleted record"
}
```

#### If a particular id doesn't exist:
Example request: `{{url}}/song/3334`

Example GET Response (400 BAD REQUEST):
```json
{
    "Message": "File not found"
}
```

## Get all records for a Specific File Type:
Endpoint: `{{url}}/{{audioFileType}}`

Example GET Request: `{{url}}/song`

Example Response (200 OK):
```json
[
    {
        "id": 22,
        "name": "Test 1",
        "duration": 250,
        "uploaded_time": "2021-03-19T07:49:19.748314"
    },
    {
        "id": 24,
        "name": "Test 2",
        "duration": 233,
        "uploaded_time": "2021-03-19T13:36:19.857718"
    },
    {
        "id": 27,
        "name": "Test 3",
        "duration": 233,
        "uploaded_time": "2021-03-21T07:44:13.501365"
    }
]
```

## Update a Record:
For updating a record, we need to specify the file type and file id in the request url, just like the GET or DELETE method, but we also need to give the fields that we need to change with the updated values. It is to be noted that, while updating a existing record, it is not required to have all the required fields (that must be in the request body when creating a file)

Endpoint: `{{url}}/`

Example request body to update the podcast `Test podcast` created above:

```json
{
    "duration": 500,
    "participants": [
        "Participant 4"
    ]
}
```

Request returns the updated file data in the response body:
Response (200 OK):
```json
{
    "id": 31,
    "name": "Test podcast",
    "duration": 500,
    "host": "Test host",
    "participants": [
        "Participant 4"
    ],
    "uploaded_time": "2021-03-21T13:22:05.923891"
}
```