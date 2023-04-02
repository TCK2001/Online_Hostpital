# Online_Hostpital
-----
# Motivation
I am currently studying abroad in Taiwan and my motivation stems from the realization that small hospitals could greatly benefit from implementing online consultations. I have developed a simple system that incorporates many useful features.
+ internet reservation through QR codes 
+ basic online consultations
+ video conferencing for medical check-ups
+ receive prescriptions at nearby pharmacies after filling out simple documents.
-----
# Languages Used
+ Python
-----
## library
+ Flask - python conntect to html
+ smtplib - email server
+ MIME(TEXT/Multipart/Image) - send/receive email
+ qrcode - qrcode
+ openai - chatgpt
+ tkinter - make UI
+ PIL - save picture
+ datetime - get time
-----
# Description
Because I tried using Flask for the first time and it felt like entering a whole new world. Initially, I was planning on implementing it with Django, but I found its syntax to be a bit different and hard to grasp right away. So, I used Flask, which is easy to connect with HTML and quickly integrate. I have added comments to all the code except for tkinter to make it easy to understand. If you have trouble understanding because it's written in Korean, please use ChatGPT or Google Translate. Thank you.
# Result
![image](https://user-images.githubusercontent.com/87925027/229334237-90afad36-623d-4d85-a8a1-002ca840e318.png)
![image](https://user-images.githubusercontent.com/87925027/229334257-0e8bee26-8104-4c65-9bb9-a3ad71521dda.png)
![image](https://user-images.githubusercontent.com/87925027/229334301-82928f73-6b46-4796-8508-053eb449bdad.png)
### You can refer to my previous post for the part where I ask questions to AI. Thank you.
![image](https://user-images.githubusercontent.com/87925027/229334339-53df678a-2e19-4f30-97c8-4299e4157089.png)
### Using Discord, it is possible to limit the number of participants to two, one doctor and one patient, for online consultations. This is not an official implementation but rather a simple implementation to restrict the number of participants.
![image](https://user-images.githubusercontent.com/87925027/229334320-b310aaac-515b-411a-8d42-89adf865ac7b.png)
