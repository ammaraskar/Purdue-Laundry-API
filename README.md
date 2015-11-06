# Purdue-Laundry-API
Scrapes purdue's wash alert/laundry page to provide a JSON API.
I personally run it on a CloudControl instance [here](https://purdue-laundryapi.rhcloud.com/),
it should be trivial to run a local
instance by installing the requirements with `pip install -r requirements.txt`
and then simply running `python start.py`


## Endpoints

There is only one endpoint right now, it returns the status of all laundry machines
in all laundry locations

###  /all

Example:

```json
{
  "Cary Quad West Laundry": [
    {
      "control_id": "28438902626234942",
      "name": "Dryer 013",
      "status": "In use",
      "time": "60 minutes left",
      "type": "Dryer"
    },
    {
      "name": "Dryer 014",
      "status": "Available",
      "type": "Dryer"
    },
    {
      "name": "Dryer 016",
      "status": "Ready to start",
      "type": "Dryer"
    }
  ],
  "Earhart Laundry Room": [
    {
      "name": "Dryer 017",
      "status": "End of cycle",
      "type": "Dryer"
    },
    {
      "name": "Dryer 018",
      "status": "Available",
      "type": "Dryer"
    },
    {
      "name": "Dryer 019",
      "status": "Available",
      "type": "Dryer"
    }
  ]
}
```

Top level keys are the name of each laundry room, in turn containing a list of the
laundry machines available in the room.
