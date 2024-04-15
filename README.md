# uchile_HR_interface
Human-Robot interface development for Bender and Jaime.
## TODO: ALL

Dear minions: 

As we've been talkin, the main idea of this project is to create a human-robot interaction interface, it MUST include:
- A speech recognition module:
  - It must run locally.
  - It must understand Spanish and English.
  - You should call it using a method called *Hear()*. The function should return a string with the recognized stuff.
- A text to speech module:
  - It must run locally.
  - The user should be able to modify, with parameters:
    - The language (English and Spanish)
    - The voice (at least 2 options)
    - The speed
  - If I publish a string in the topic *speak*, the robot must say what I sent.
  - You can also be able to call it by using the function *Say(str: string)*.
  - The user should be able to stop de speech at any time by sending a command.
    - Ex: If the robot is speaking a very long speach, and I want to interrupt it, I should be able to stop it by sending the command: *speach.stop()*

PLEASE follow the gitflow: 
- Develop the project on the *develop* branch
- DON'T write code directly on the *main* branch
- DON'T merge the *main* branch into the *develop* branch
