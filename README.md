# Curseduca Track Creator

Curseduca Track Creator is an automation tool that helps companies gain control over Curseduca students' contents in their platform. A practical use for this is for controlling the regulamentary training tracks. 

I.E.: In order for the student to advance to the next course, the previous course must be completed and evaluated by the manager. So the manager checks if he is able to advance and releases the new course.

The Python code runs on Zapier and receives data sent from Typeform to communicate with the Curseduca APIs.

The steps are:

![image](https://github.com/user-attachments/assets/83ffb495-5002-4f3a-838d-9c3d69d9baaf)

## I. Typeform

Manager picks what action should be done:
- Create new member
- Update existing member
- Inactivate member
- Create tracks
- Release content

Each action will generate a variable that will be sent to Zapier to be interpreted by the script.

The following step is to fill the form with the data needed. Such as e-mail, name and contents. 

## II. Zapier

The completion of the form will trigger a Zap run. 

This run will receive the data from the Typeform, transform it when needed and follow the pipeline the action variable defined in the previous step.

## III. Curseduca

Curseduca will receive the data sent by the manager and process it accordingly from the action.
