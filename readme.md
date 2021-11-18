User access control system
Contents
Analysis
Problem: 2
Stakeholder: 3
Existing solutions: 5
Key features of the solution: 8
Limitations of the solution: 10
Hardware and software requirements: 11
Success criteria: 13

Problem:
The system that is being created will serve the function of a door lock with user authentication to grant access and video recording accompanied by a phone application and website were the events (movement and people entering) and the recordings will be viewable by the user. A stakeholder would have a door that leads to an area that is meant to have restricted access that only authorised people should be able to access, whilst also recording all events. The events that are being recorded should be anything that happens outside the door, being detected by an infra-red motion detector. All of the events will be recorded, whether that be someone entering or someone trying to enter or tamper with the door. The system should unlock the door when an authorised person wishes to go in, being checked by a RFID card reader. All the information should then be available for the stakeholder in an app or website, with events being displayed, whether it was someone entering or movement outside accompanied with video recordings of what happened.
Advantages over non computational method:
By using a microcomputer, the movement of each person is automatically recorded, meaning if they attempt to access the area there will be a record of this accompanied by a recording to show what they did, this is not possible to achieve this with a non-computational method. The video recordings and log will be saved to a sever providing easy access to the video recordings and logs, through the website or phone app or the. Neither of which would be possible with a no computational method such as a pen and paper sign in sheet. Furthermore, if the door had to be locked at all times apart from when someone authorised needs to enter, then the key would have to be given to everyone who can enter or have someone at the door at all times to unlock it for them. The possible issue with someone having the key is that it may get taken from them, this issue could happen with a RFID card however a second factor of authentication could be put in place with each user having an individual code that is liked to their card, meaning that both parameters have to be met to allow access.
There is a clear advantage of the job being done by a commuter system over a human, and this is that you do not need someone at the entrance of the door all the time, and it in most cases can be unmanaged, with video recording and complete logs. If a human were to do this job, then there would be lots of functions for them, including noting down everyone who enters, unlocking the door as well as making sure that people entering the area are authorised to do so, all of which is easily achievable by a computer system.

Stakeholder:
The stake holder is named Daniel, they work at a technology company and have been tasked with finding a way to control access to an area whilst having video recording capabilities, all feeding back the information to an app. Once the system is setup, they plan to leave company security to be responsible for the use and monitoring of it.
I was connected with the stakeholder through a mutual friend, the first interaction went as followed:
Jonathan – ‘Hi Daniel, my name is Jonathan, and I heard that you have an area that needs to have access control, and I was wondering if I would be able to build you a system that helps with that.’
Daniel – ‘Sure, that sounds great, is there anything that you need from me?’
Jonathan – ‘Let me send you over some questions that will allow me to better understand the issue’
Questions with stakeholder:

1. Question: Do you use any currently marketed solutions, such as ring doorbell for monitoring or a ‘build your own’ style system for user entry? Do these work as you want? If not, what could be improved?

Answer: ‘I do currently use a ring doorbell system; however, it does not contain the necessary features to allow integration with a RFID-based security system, further forms of user authentication would be welcomed as the ring doorbell system is an isolated platform.’

2. Question: Do you have any special requirements for the hardware or software of the solution or application?

Answer: ‘An easy way to look at the history of ‘events’ and spot people who are attempting to enter at obscure times e.g. late at night.’

3. Question: Is there a pre-existing network storage location?

Answer: ‘No, we have no pre-existing network storage location for this capture data.’

4. Question: Is the system going to be in a high traffic area (lots of people walking past the sensor)?

Answer: ‘No, it would be at the entrance to a floor of an office building, so the only people triggering the sensor would be those attempting to enter.’
Requirements from stakeholder:
From my conversation with the stakeholder, I have established that there are 3 key requirements that they have for the solution:

1. RFID based door lock
2. Video recording of all events
3. Notifications from the app alerting them of any events that happen
   The stakeholder mentioned that additional user authentication would be welcomed by them, this could be done in the form of matching the users face from the video to the id card that is being used to enter, this would be done through facial recognition.
   Why the solution is appropriate for the stakeholder:
   The key requirements that have been given to me by the stakeholder are have all already been intended to be put in place in the system, and the additional request of further user authentication can be put in place at the end of the project if there is still time.

Existing solutions:
Ring doorbell:
Ring doorbell is a commercial video recording doorbell that allows the owner to see a live video feed and communicate with people outside. The doorbell can be motion activated or activated by a push of the button on the unit and will send a push notification to the owners’ devices. The video recording is saved to the cloud and then deleted after 60 days. This functionality however does require a monthly subscription of £2.50 monthly. The video recordings can be viewed in the phone app on the user’s phone or on the computer. The issue with this solution is that it does not connect to a lock of the door meaning it cannot control the access to it, nor is it able to recognise people meaning that someone would always have to be able to check if the person is meant to be able to enter and if so then let them in whether that be in person or through a 3rd party solution.

Ring doorbell app
Generic RFID deadbolt door lock:
Multiple examples of an RFID based door lock can be found on amazon as well as other online retailers, one example that I have found is below. It is an all-in-one unit, that lock the door with a bolt opposed to an elector-magnet, this means the lock is redundant to power loss, meaning if there is power loss it will not unlock. The lock has 2 ways of entry, the phone app and the RFID cards. The issue that I see with the system is that the cards are generalised meaning when someone enters, it does not log who it is which means that if an issue has arisen, then it is harder to trace who was the cause of the issue. A recording system would have to be separate to the lock, this would cause the integration of the 2 systems to be complicated and a lengthy process and may not even be possible.

Akuvox R20A (example of a multi part solution):
To find a product that is closest to mine, I reached out to a company called DSSceurity. I found a product called the Akuvox R20A that they sell, it is a RFID based intercom system that can allow users in as well as direct communication with anyone at the door. The recommended retail price of just the product is £270, one would have to buy the relays, exit button and door magnet separately. The system has a linked app which the user can use to interact with people at the door, and the system is set up through a web portal. After looking through the product description and talking to the representative further, I have found a few key features of the product. It is connected to the internal network through a Power Over Ethernet cable, this means that there is only one cable that is responsible for both power and internet access. The door can be opened remotely, meaning if someone does need access that does not have a card on them or assigned to them, then it can be opened when needed. The camera features infra-red LEDs, meaning that it will function at night as well as during the day, it also does include a light. A limitation that I have identified from the product is that the recordings are not saveable natively, meaning that you could set up a constant feed and screen record that however, that is inefficient and would require another computer dedicated to doing so. The end user would also have to have the other necessary parts for the system such as the magnet, relay box and a release switch, however it is common for solutions such as this, doing so allows the user to set the system up how will suit them best.

What will be done to improve upon these solutions:
All of the systems inherently have advantages and disadvantages, for the ring doorbell, it allows the user to interact with someone at the device side, this means that if there is an issue it should be quickly resolved. The ring doorbell also allows for a live video feed from the camera which means that the event that is happening will be viewable before it is over. As the ring doorbell does not have a lock integrated with it, it could be set up that the person at the other end of the door could open the door remotely, but this would be more complicated that an all-in-one solution.
The RFID door lock allows for unlocking through the app, this means that the user is able to grant access to someone if it is needed without having to add their id card to the database. The lock is battery powered meaning that if the battery dies, you have to wait until it is recharged, there is also the potential issue of someone being on the wrong side of the door when the battery dies, this potentially could he a health and safety issue if there is a fire. This system however does not include video recording so if it was needed, like it is for the stakeholder, then it would have to be done separately, and then they would not be easily integrated.
The final solution that is looked at only has the issue of the events from the door not being recorded, this may not be an issue for all of the customers, but in the stakeholders case it is. Previously I mentioned that one could scree record the live feed of the door, but there would certainly issues that would have to be looked at, such as dedicating a computer for this, what happens in the case of a power outage, who will restart the recording and when, as well as the file size of the recordings, as it will probably be much larger than if it were the direct feed from the system.
From all the systems that have been looked at, some key features have stood out, one of which is the live video, and I will be looking into setting up a network stream, and then also saving video when the events happen. In this use case the communication between someone at the door and the user is not needed but flagging abnormal entrance times will be.

Key features of the solution:
The recording will only begin when motion is detected, this is done in order to reduce amount of storage needed for the system.
The phone application:
The phone application will allow the end user to view a list of the events that have previously occurred outside of the door, and view the video footage of those events. The application will highlight any events that are outside of normal hours, which will increase the functionality of the system. The stakeholder has mentioned about the possible ability to remotely lock and unlock the door which will be controlled through the app, this increases the use of the system and gives it advantages over other commercially available systems.
The sensor:
The sensor used is infra-red, meaning that only people will set it off. The sensor also has adjustable temperature compensation, meaning that this can be adjusted depending on the environment that it is in. If it is the case that the system is in a high-volume area, the angle and range of the motion sensor can be adjusted in order to combat a large number of false recordings which would result in higher storage capacity being needed and more flags on the app.
The microcomputer:
The microcomputer running the system will be on the side of the door that would be considered the exit to prevent tampering to the system. The microcomputer used a raspberry pi, meaning that it is inexpensive, yet it is robust. As a raspberry pi is being used instead of an Arduino, it has a desktop and therefore can easily be VNC or SSHd into if there is an issue and can easily be resolved.
The camera:
The camera is a webcam, meaning that it is relatively inexpensive but still suited for long term continuous recording if the system is in a high-volume area. If the system is later set up for face recognition of the users in order to confirm identity, then it may be an issue, however this can be delt with by using the camera to train the model with the faces of the users.
RFID scanner:
The RFID scanner is a low voltage and therefore it has a lower range compared to a more powerful one meaning that it will not be triggered if someone with an authorised card is too close to the door.
Due to all the aforementioned points, the solution that is being made will work as intended, and optimise it for its use case. The stakeholder has also mentioned that they may want to be able to unlock and lock the door from the app in case they need to let anyone in.

Limitations of the solution:
The phone application:
The application is for an iPhone, they tend to have less powerful hardware as the apps and code are more streamlined, meaning if the code of the app is not efficient then there will be possible issues that may arise. The app will have the functionality to lock and unlock the door, meaning that the communication between the phone and system should be secured, however this may not be the case.
The magnet:
The electro-magnet that will be locking the door is non redundant, meaning that if power is cut to the microcomputer, or the additional power source connected to the relay runs out, then the magnet will disengage and the door will unlock. This means that the entire system can be null voided by a power cut. What can be done in order to prevent this is connect the system to a UPS. The magnet is also a low power one but it can be substituted for one that is higher strength, however, that would also require a more powerful power source and possibly a higher quality relay.
RFID cards:
The RFID cards are not encrypted, this means that they can be cloned easily by a third party if they wish to get access, as each card is unique to the holder, the person that is managing the system is able to view the video recordings and logs to see if the people entering match the cards that are used. However, as this would class as a normal event, the user would not be alerted. This is unless the system is accessed outside of work hours, and this will send an alert out due to the abnormal behaviour.
Camera:
At the moment the system will not offer a live camera view due to the hardware limitations of the camera as well as the microcomputer that the system will be running off. The camera that is being used is a standard webcam and it does not offer high video quality meaning that it will not be effective for identifying people far away from it.
Microcomputer:
The microcomputer being used has a low compute power relatively, this meaning it may struggle to handle all of the required functions of it, these will include running the sensor and recording, MQTT server for the iOS application and if the facial recognition that is planned to be implemented down the line. There may be a storage issue with the system as the primary storage device is a 16Gb microSD card, if needed, an external hard drive could be added, this would make the system have a larger footprint, or it may be connected to a network storage location if needed.
Hardware and software requirements:
Hardware:
The stakeholder has set out no specific hardware requirements for this solution, however the system will be using components that are suited for long term deployment in order to minimise the risk of a system failure due to component error.
The phone application will be running on iOS, meaning that the user would have to have an iPhone.
Hardware requirements for micro-computer:
• Motion detector connected to detect motion
• Camera connected to board to record video
• Relay connected to board to turn on and off magnet
o Magnet connected to relay to hold door closed
• Power supply connected to board to provide power

    Software:

The stakeholder has requested that the application will send them push notifications when specific events happen, such as access to the area when outside of work hours, and prolonged movement outside the door. This will be done in the phone app and I will further discuss with the stakeholder whether or not they want email notifications as well. The only other software requirement is that there be an easy-to-understand UI, that will not encounter failures when being used, as its goal is to keep an area secure and if a failure occurs this may not be done as the app may have the ability to lock and unlock the door.
The phone application will be running on iOS, meaning that the user will have to have an iPhone with up-to-date OS.
App requirements:
• Login system
o Create users
o Verify via email
o Link account to the system
• App menu
o View events
 View the recordings of specific events
 Highlight irregular time events and blocked entrances
 Show time that events lasted
 Show who entered if someone did
o View recordings
• Push notifications for events
• Ability to lock and unlock door
o Possibility to keep door locked

Success criteria:
Main criteria:
Criteria How to show
Recording to start on the detection of motion Compare timestamp of recording starting in the app and time of the movement occurring
System to allow access for only authorised users when card is scanned Try unlocking the door with an authorised and unauthorised card
Door to relock after set amount of time after unlock Screen shot of code
Internal button to allow users to exit the door Photo of the button opening the door
Logs show who entered and at what time Screen shot from the app
Functional login system, with the ability to add a new account Screen shot form login page and once logged in
System to start on boot of device in case of power loss Restart microcomputer and screen shot once code begins to run
Have in app video playback of recorded events Screen shot of video playback in app
Have notifications sent to the user, when door accessed out of core business hours Screen shot of the notifications within reasonable time
Compact hardware in order to have a small footprint Photo of hardware
Create a database of authorised people to enter Screen shot of code
Create a database for the login system Screen shot of code
Be able to view if an event was a prolonged length of time in the app Screen shot of app
Secondary criteria:
Criteria How to show
Door to relock after set amount of time after unlock Screen shot of code
Functional login system, with the ability to add a new account Screen shot form login page and once logged in
Have notifications sent to the user, when door accessed out of core business hours Screen shot of the notifications within reasonable time
Compact hardware in order to have a small footprint Photo of hardware
Create a database of authorised people to enter Screen shot of code
Be able to view if an event was a prolonged length of time in the app Screen shot of app

Luxury criteria:
Have face recognition compare the face of the person unlocking the door, with the cardholder Screen shot of the percentage likely hood that it is the correct user
Allow the door to be locked/unlocked through the app Screenshot of feature inside of app
