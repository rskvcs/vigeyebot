# VigEye bot

VigEye bot is built using [RASA ](https://rasa.com/)stack

## Installation
run the following command:
```
pip install -r requirements.txt
```
## Files structure

- **__init__.py**: An empty file that helps python find your actions.
- **actions.py**: Code for your custom actions
- **config.yml**: Configuration of your NLU and Core models
- **credentials.yml**: Details for connecting to other services
- **data/nlu.md**: NLU training data
- **data/stories.md**: stories
- **data/lookup_tables**: Lookup tables for departments and states
- **data/json**: Nodal officers data
- **domain.yml**: assistant’s domain
- **endpoints.yml**: Details for connecting to endpoint channels
- **models/<timestamp>.tar.gz**: Your initial model. The timestamp is in the format of YYYYMMDD-hhmmss. NLU-only models will have nlu prefix at the front

## Training data preparation and format

### Intent
To create intent, following format to be used **## intent:name_of_intent** followed by a list of questions for the intent (space between each intent):
```
## intent:affirm
- yes
- of course
- sure
- yeah
- ok
- cool
```
### Entity
An entity can be specified inside each question as **[value](name of entity)**
```
## intent:state_nodal_officer
- who is the nodal officer for [Karnataka](states) state
```
### Lookup table
Lookup tables are used to store a long list of values for a single entity. There are two ways to do it, one to include them in-line and another as text file.
```
### lookup:departments
  data/lookup_tables/departments.txt
```

## Stories
Rasa stories are a form of training data used to train the Rasa’s dialogue management models.
Example of a dialogue in the Rasa story format:
```
## Greeting

* greet
    - action_greet_by_time
    - utter_greet_user
    - greet_user
```
**More information: [https://rasa.com/docs/rasa/core/stories/](https://rasa.com/docs/rasa/core/stories/)**

## Custom Actions
RASA provides SDK to build and interact with custom action server written in python. Action server endpoint has to be specified in “endpoints.yml” to use the same. Please check the actions.py for more details.
```
action_endpoint:
  url: "http://localhost:5055/webhook"
```
**More information: [https://rasa.com/docs/rasa/core/actions/#custom-actions](https://rasa.com/docs/rasa/core/actions/#custom-actions)**

## Training and testing 
### Training
To train a model that combines a Rasa NLU and a Rasa Core model
Run `rasa train`
### Testing 
**To test via shell mode run the following command**
`rasa shell`

**To start an interactive learning session, run**
`rasa interactive`

**To test a specific model, run**
`rasa shell -m models/20200105-112742.tar.gz`

**More information: [https://rasa.com/docs/rasa/user-guide/command-line-interface/#train-a-model](https://rasa.com/docs/rasa/user-guide/command-line-interface/#train-a-model)**

## Running Server
### NLU Server
Run the following command
`rasa run --enable-api -m models/20200105-112742.tar.gz --cors "*"`

**More information: [https://rasa.com/docs/rasa/user-guide/command-line-interface/#start-a-server](https://rasa.com/docs/rasa/user-guide/command-line-interface/#start-a-server)**

### Custom Action Server
`rasa run actions`
**More information: [https://rasa.com/docs/rasa/user-guide/command-line-interface/#start-an-action-server](https://rasa.com/docs/rasa/user-guide/command-line-interface/#start-an-action-server)**

### Evaluating models
## Evaluating an NLU model
**Split nlu training data**
 `rasa data split nlu`

**To test the NLU model prediction** 
`rasa test nlu -u test_set.md --model models/20200105-112742.tar.gz`

**To test cross-validation without creating a separate test set, run**
`rasa test nlu -u data/nlu.md --config config.yml --cross-validation`






