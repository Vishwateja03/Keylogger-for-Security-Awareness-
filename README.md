# Keylogger-for-Security-Awareness
In the digital era, information security is paramount due to increasing threats from cyberattacks 
and unauthorized data access. This project focuses on developing a keylogger for security 
awareness to demonstrate potential vulnerabilities in computing systems and emphasize the 
importance of securing sensitive information. The keylogger is a Python-based application 
designed to monitor, record, and securely store user activity, including keystrokes, clipboard 
content, screenshots, and system information. 
The implementation integrates modules for capturing user inputs and system data while 
ensuring data confidentiality through cryptographic encryption using the Fernet symmetric 
encryption algorithm. Collected data is periodically sent to a remote server via HTTP POST 
requests and optionally transmitted via email for centralized analysis. The system leverages 
Python libraries such as pynput for keylogging, win32clipboard for clipboard monitoring, 
ImageGrab for capturing screenshots, and sounddevice for audio recording. This project 
illustrates the functionality of keyloggers as an educational tool to raise awareness about cyber 
threats and highlight the need for robust defensive mechanisms. 
The outcome of the project serves as a technical demonstration, emphasizing the significance 
of implementing security measures such as multi-factor authentication, anti-keylogging tools, 
and encrypted communication to protect against similar threats in real-world scenarios. This 
work contributes to the broader field of cybersecurity by providing insights into attack vectors 
and promoting a proactive approach to information security.
