# Finger_scanner_auth

We created this project as part of a 24 hour hackathon event. We made this application to meet the needs of a local company who wanted a way to validate customers coming to member only event. Originally we had planned to do this with a biometric finger scanner, and when we could not get that specific hardware to interact with our program, we pivotted to validate people using a PIN and picture system (thus the misnomer). 

We created this as a Django web application that uses a SQL database to store all of the member information. It is a super customizable application that allows the company to grow in the future, adding more customers, membership types, and events. The web application has a few options, create member edit member delete member, Create new perk(membership package), and run events.

There is also some customization that can be done in the code to allow the picture to be taken from a USB connected webcam rather than your laptops native webcam.

