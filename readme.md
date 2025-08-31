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

- [Mostly ~done] Appointment time constraints + selection. Now with a working implementation of appointment time reservation. A customer can book for, say, 12:00PM, then the next customer that attempst to book for this time will be met with an error telling them this timeslot clashes with another customer's appointment. 
- [To-do] CSS styles