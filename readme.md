# Prerequisite(s)
- Python v3.12.10 
    - Mainly for compatibility with the previous project's application; breaks on newer versions.


# Running this webapp:
Make sure you are in the correct directory (CSE5IDP-Project) where app.py is accessible.

```
pip install flask
python app.py
```


# Notes:

- [WIP] Appointment time constraints + selection. So far I can only make it so that the customer can pick an hourly time, but not half-hourly.
    - Back-end-sided validation for time selection; throw an error at  customer for picking a time like 12:37PM. It must be a valid (half-)hourly time for an appointment. 
- [To-do] CSS styles