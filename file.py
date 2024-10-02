import gspread
from oauth2client.service_account import ServiceAccountCredentials

#libraries for email 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

# libraries for lost section 
import cv2 
from skimage.metrics import structural_similarity as compare_ssim
import imutils
import numpy as np
import matplotlib.pyplot as plt 
import requests
import os
import time 

threshold =0.3


# Email credentials and settings
   
# Authenticate using the credentials JSON file you downloaded
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# change the file in gitignore and add the file in the same directory

creds = ServiceAccountCredentials.from_json_keyfile_name('credSheetsDemo.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheets document by its title
spreadsheet = client.open("LostAndFound")

# Access a specific worksheet (sheet) within the document
worksheet = spreadsheet.get_worksheet(0)  # Assuming responses are in the first sheet

# Get all responses as a list of dictionaries
responses = worksheet.get_all_records()

# Create dictionaries to store lost and found items
lost_items = {}
found_items = {}

# Process responses
for response in responses:
    tStamp = response['Timestamp']
    email_address = response['Email Address']
    itemLF = response["Item lost or found"]
    name = response["Your name"]
    contact_info = response["Your Contact info"]
    item_name = response["Item Name"]
    description = response['Item description']
    category = response["Item category"]
    brand = response['Item brand']
    attachments = response.get('Attachments', '').split(',')   # Need to check this urgent.

    
    
    

    # Add item to the appropriate dictionary based on lost/found status
    if itemLF.lower() == "lost":
        lost_items[item_name] = {
            'category': category,
            'description': description,
            'brand': brand,
            'contact_info': contact_info,
            'name': name,
            'email': email_address,
            'attachments': attachments
        }
    elif itemLF.lower() == "found":
        found_items[item_name] = {
            'name': name ,
            'contact_info': contact_info,
            'category': category,
            'description': description,
            'brand': brand,
            'attachments': attachments
        }

ssim_score = -111111
    # Match found items with lost items
for found_item_name, found_item in found_items.items():
    message = MIMEMultipart() 
    subject = "ssss"
    to_email ="nope"
    found_item_category = found_item['category']
    found_item_description = found_item['description']
    found_item_brand = found_item['brand']
    print (found_item['name'])
    subject = " "
    to_email= " "

    # Search for matching lost items
    for lost_item_name, lost_item in lost_items.items():
        if (
            lost_item['category'] == found_item_category and
            (found_item_description in lost_item['description'] or found_item_brand in lost_item['brand'])
        ):  ## Change here like inverse comparison here needs to be done to improve the code
            # Send email to the person who lost the item
            subject = f"Your lost item '{lost_item_name}' has been found!"
            Emessage = f"Your {lost_item_name} has been found. Please contact {found_item['name']} at {found_item['contact_info']} for details."
            print(Emessage)
            EmessageD = MIMEText(Emessage)
            message.attach(EmessageD)
            to_email = lost_item['email']
            
            attachment_image =" "
        if found_item['attachments']:
            for attachment_url in found_item['attachments']:
                # Read the image from the attachment URL
                url_____ = attachment_url.split('id')[1]
                print(url_____)
                attachment_url = "https://drive.google.com/uc?id" + url_____
                response = requests.get(attachment_url)
                if response.status_code ==200:
                    attachment_content =response.content
                    try:
                        attachment_image = cv2.imdecode(np.frombuffer(attachment_content, np.uint8), cv2.IMREAD_COLOR)
                        time.sleep(3)
                        if attachment_image is None:
                            print("Image decoding failed for attachment image.")
                            attachment_filename = "attachment_image.jpg"  # Change the filename as needed
                            cv2.imwrite(attachment_filename, attachment_image)
                            continue
                    except Exception as e:
                        print(f"Error decoding attachment image: {e}")
                        continue
                # Compare the attachment image with each lost item's image

             
          
                for lost_attachment_url in lost_item['attachments']:
                    url_____ = lost_attachment_url.split('id')[1]
                    print(url_____)
                    lost_attachment_url = "https://drive.google.com/uc?id" + url_____
                    response = requests.get(lost_attachment_url)
                    if response.status_code ==200:
                      lost_attachment_content = response.content
                      lost_attachment_image = cv2.imdecode(np.frombuffer(lost_attachment_content, np.uint8), cv2.IMREAD_COLOR)

                    if attachment_image.shape == lost_attachment_image.shape: 
                        try:

                            # win_size = min(attachment_image.shape[0], attachment_image.shape[1], 7)  # Adjust as needed
                            # ssim_score = compare_ssim(attachment_image, lost_attachment_image, win_size=win_size, multichannel=True)
                            # print(ssim_score)
                            # attachment_image = np.squeeze(attachment_image)
                            # lost_attachment_image = np.squeeze(lost_attachment_image)

                            # smaller_side = min(attachment_image.shape[:2])
                            # win_size = min(smaller_side, 7)  # Use smaller_side as the upper limit
                            # if win_size % 2 == 0:
                            #   win_size -= 1  # Ensure it's an odd value
                            # ssim_score = compare_ssim(attachment_image, lost_attachment_image, win_size=win_size)
                            # print(ssim_score)
                           attachment_gray = cv2.cvtColor(attachment_image, cv2.COLOR_BGR2GRAY)
                           lost_attachment_gray = cv2.cvtColor(lost_attachment_image, cv2.COLOR_BGR2GRAY)

            # Calculate SSIM using grayscale images
                           (ssim_score,diff) = compare_ssim(attachment_gray, lost_attachment_gray,full= True)
                           
                           diff = (diff * 255).astype("uint8")

# 6. You can print only the score if you want
                           print("SSIM: {}".format(ssim_score))
                           
                            
                        except AttributeError:
                             ssim_score =0
                        print(ssim_score)
                    else :
                        print ("hooole")
        if ssim_score > threshold :
            try:
                
                for attachment_url in found_item['attachments']:
                # Download image
                  url_____ = attachment_url.split('id')[1]
                  print(url_____)
                  attachment_url = "https://drive.google.com/uc?id" + url_____
                  response = requests.get(attachment_url)
                  print(attachment_url)
                  img_data = response.content
                
                  img = MIMEImage(img_data, 'jpg')
                # img = MIMEBase('application', 'octet-stream')
                # img.set_payload(img_data)
                # encoders.encode_base64(img)
                  img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_url))
                  img.add_header('Content-ID', f'<{attachment_url}>')
                #   img.add_header('X-Attachment-Id', f'{attachment_url}')
                  message.attach(img)
                  
           

           
        #  # Exit loop after sending email
            except AttributeError:
                print("Yaar url ki maa ki ")
          
        #  send_email(subject, message, lost_item['email'])
        
        #  print(f"Email sent to {lost_item['email']} for lost item '{lost_item_name}'")
    #  change the email address to the email from which u want to send the email reply 
    email_address = 'randomusermanas1@gmail.com'
    email_password = 'evvljoypsecsqzgw'
    
    message['From'] = email_address
    message['To'] = to_email
    print(to_email)
    message['Subject'] = subject
        # msg.attach(MIMEText(message, 'plain'))

        # Connect to the server and send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
        
    # print(message.as_string())  
    server.sendmail(email_address, to_email, message.as_string())
    server.quit()
    # message.attach(None)
    # Clear the email content and attachments
    message.set_payload(None)  # Clear the content

    # Clear attachments
    message._payload = []  # Clear the payload, removing all parts

    # Clear the headers
    message.replace_header('Subject', '')  # Clear the subject
    message.replace_header('From', '')     # Clear the "From" address
    message.replace_header('To', '')       # Clear the "To" address


    print("Processing completed.")
    time.sleep(10)

# Check name of the memor who lost it in console printing other things working fine