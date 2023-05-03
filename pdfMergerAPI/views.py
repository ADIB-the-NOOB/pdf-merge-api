from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import glob, json, re, cv2
import os, shutil, pikepdf
from PIL import Image
from PyPDF2 import PdfMerger, PdfFileReader, PdfFileWriter
import img2pdf, pdf2image
from django.http import FileResponse
import numpy as np
#from pdfMergerAPI.settings import STATIC_URL
from selenium import webdriver
import time, base64
import pytesseract
from PIL import Image
import logging
import easyocr

class homepage(APIView):
    def get(self, request):
        return Response({'Status': 'GET method not allowed! Use POST for accessing API!'}, status=status.HTTP_400_BAD_REQUEST)

USERNAME = 'BALAJIENTR-A'
PASSWORD = 'Admin@1'

class addUser(APIView):
    def post(self, request):
        jsonReceived = request.data
        if not 'vle_id' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "vle_id missing."})
        elif not 'vle_name' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "vle_name missing."})
        elif not 'location' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "location missing."})
        elif not 'contact_person_name' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "contact_person_name missing."})
        elif not 'pincode' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "pincode missing."})
        elif not 'state' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "state missing."})
        elif not 'phone_no' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "phone_no missing."})
        elif not 'mobile_no' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "mobile_no missing."})
        elif not 'email' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "email missing."})

        elif not 'utiuserid' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "utiuserid missing."})
        elif not 'utiuserpassword' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "utiuserpassword missing."})
        USERNAME = jsonReceived['utiuserid']
        PASSWORD = jsonReceived['utiuserpassword']
        if not USERNAME or not PASSWORD:
            return Response({"Message": "Failed!", "Reason": "Check your username and password!"})
        chrome_settings = webdriver.ChromeOptions()
        chrome_settings.add_argument('--headless')
        chrome_settings.add_argument('--no-sandbox')
        chrome_settings.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
        driver = webdriver.Chrome('pdfMergerAPI/chromedriver', options=chrome_settings)
        attempts = 0
        url = ''
        successFlag = 0
        while True:
            driver.get('https://www.psaonline.utiitsl.com/psaonline/showLogin')
            captcha = driver.find_element_by_xpath('//*[@id="PsaLoginAction"]/table/tbody/tr[8]/td/img')
            img_captcha_base64 = driver.execute_script("""
                                                        var ele = arguments[0];
                                                        var cnv = document.createElement('canvas');
                                                        cnv.width = ele.width; cnv.height = ele.height;
                                                        cnv.getContext('2d').drawImage(ele, 0, 0);
                                                        return cnv.toDataURL('image/png').substring(22);    
                                                        """, captcha)
            with open(r"captcha.png", 'wb') as f:
                f.write(base64.b64decode(img_captcha_base64))
            img = Image.open('captcha.png')
            captchaText = pytesseract.image_to_string(img)
            # print(captchaText)
            userField = driver.find_element_by_xpath('//*[@id="PsaLoginAction_userId"]')
            userField.send_keys(USERNAME)
            passField = driver.find_element_by_xpath('//*[@id="PsaLoginAction_password"]')
            passField.send_keys(PASSWORD)
            captchaField = driver.find_element_by_xpath('//*[@id="PsaLoginAction"]/table/tbody/tr[10]/td/input')
            captchaField.send_keys(captchaText)
            
            attempts += 1
            if driver.current_url == 'https://www.psaonline.utiitsl.com/psaonline/PsaLoginAction.action' or attempts>=10:
                if not attempts>=10:
                    successFlag = 1 
                break
            else:
                time.sleep(2)
            
        # time.sleep(2)
        if successFlag == 1:
            try:
                driver.get('https://www.psaonline.utiitsl.com/psaonline/createUser')
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="addVle_vId"]').send_keys(jsonReceived['vle_id'])
                driver.find_element_by_xpath('//*[@id="addVle_vName"]').send_keys(jsonReceived['vle_name'])
                driver.find_element_by_xpath('//*[@id="addVle_vLocation"]').send_keys(jsonReceived['location'])
                driver.find_element_by_xpath('//*[@id="contactPerson"]').send_keys(jsonReceived['contact_person_name'])
                driver.find_element_by_xpath('//*[@id="addVle_vPincode"]').send_keys(jsonReceived['pincode'])
                stateCode = ''
                state = jsonReceived['state'].upper().strip()
                if state == 'ANDAMAN AND NICOBAR ISLANDS':
                    stateCode = '//*[@id="vState"]/option[2]'
                elif state == 'ANDHRA PRADESH':
                    stateCode = '//*[@id="vState"]/option[3]'
                elif state == 'ARUNACHAL PRADESH':
                    stateCode = '//*[@id="vState"]/option[4]'
                elif state == 'ASSAM':
                    stateCode = '//*[@id="vState"]/option[5]'
                elif state == 'BIHAR':
                    stateCode = '//*[@id="vState"]/option[6]'
                elif state == 'CHANDIGARH':
                    stateCode = '//*[@id="vState"]/option[7]'
                elif state == 'CHHATTISGARH':
                    stateCode = '//*[@id="vState"]/option[8]'
                elif state == 'DADRA AND NAGAR HAVELI':
                    stateCode = '//*[@id="vState"]/option[9]'
                elif state == 'DAMAN AND DIU':
                    stateCode = '//*[@id="vState"]/option[10]'
                elif state == 'DELHI':
                    stateCode = '//*[@id="vState"]/option[11]'
                elif state == 'GOA':
                    stateCode = '//*[@id="vState"]/option[12]'
                elif state == 'GUJARAT':
                    stateCode = '//*[@id="vState"]/option[13]'
                elif state == 'HARYANA':
                    stateCode = '//*[@id="vState"]/option[14]'
                elif state == 'HIMACHAL PRADESH':
                    stateCode = '//*[@id="vState"]/option[15]'
                elif state == 'JAMMU AND KASHMIR':
                    stateCode = '//*[@id="vState"]/option[16]'
                elif state == 'JHARKHAND':
                    stateCode = '//*[@id="vState"]/option[17]'
                elif state == 'KARNATAKA':
                    stateCode = '//*[@id="vState"]/option[18]'
                elif state == 'KERALA':
                    stateCode = '//*[@id="vState"]/option[19]'
                elif state == 'LADAKH':
                    stateCode = '//*[@id="vState"]/option[20]'
                elif state == 'LAKSHADWEEP':
                    stateCode = '//*[@id="vState"]/option[21]'
                elif state == 'MADHYA PRADESH':
                    stateCode = '//*[@id="vState"]/option[22]'
                elif state == 'MAHARASHTRA':
                    stateCode = '//*[@id="vState"]/option[23]'
                elif state == 'MANIPUR':
                    stateCode = '//*[@id="vState"]/option[24]'
                elif state == 'MEGHALAYA':
                    stateCode = '//*[@id="vState"]/option[25]'
                elif state == 'MIZORAM':
                    stateCode = '//*[@id="vState"]/option[26]'
                elif state == 'NAGALAND':
                    stateCode = '//*[@id="vState"]/option[27]'
                elif state == 'ODISHA':
                    stateCode = '//*[@id="vState"]/option[28]'
                elif state == 'OTHER':
                    stateCode = '//*[@id="vState"]/option[29]'
                elif state == 'PONDICHERRY':
                    stateCode = '//*[@id="vState"]/option[30]'
                elif state == 'PUNJAB':
                    stateCode = '//*[@id="vState"]/option[31]'
                elif state == 'RAJASTHAN':
                    stateCode = '//*[@id="vState"]/option[32]'
                elif state == 'SIKKIM':
                    stateCode = '//*[@id="vState"]/option[33]'
                elif state == 'TAMILNADU':
                    stateCode = '//*[@id="vState"]/option[34]'
                elif state == 'TELANGANA':
                    stateCode = '//*[@id="vState"]/option[35]'
                elif state == 'TRIPURA':
                    stateCode = '//*[@id="vState"]/option[36]'
                elif state == 'UTTAR PRADESH':
                    stateCode = '//*[@id="vState"]/option[37]'
                elif state == 'UTTARAKHAND':
                    stateCode = '//*[@id="vState"]/option[38]'
                elif state == 'WEST BENGAL':
                    stateCode = '//*[@id="vState"]/option[39]'
                if not stateCode:
                    return Response({"Message": "Failed!", "Reason":"Invalid state name!"})
                    # //*[@id="vState"]/option[2]
                driver.find_element_by_xpath('//*[@id="vState"]').click()
                driver.find_element_by_xpath(stateCode).click()
                driver.find_element_by_xpath('//*[@id="addVle_vPhone"]').send_keys(jsonReceived['phone_no'])
                driver.find_element_by_xpath('//*[@id="vMobile"]').send_keys(jsonReceived['mobile_no'])
                driver.find_element_by_xpath('//*[@id="vEmail"]').send_keys(jsonReceived['email'])
                driver.find_element_by_xpath('//*[@id="vPan"]').send_keys(jsonReceived['pan'])
                # driver.quit()
                driver.find_element_by_xpath('//*[@id="addVle_0"]').click()
                time.sleep(2)
                try:
                    if driver.find_element_by_xpath('//*[@id="dialog-message"]/p').text.strip() == "Vle id already exists. Kindly use different Id.":
                        return Response({"Message": "Failed!", "Reason": "VLE ID already exists!"})
                    elif driver.find_element_by_xpath('//*[@id="dialog-message"]/p').text.strip() == "Record Added Successfully.":
                        return Response({"Message": "Record Added Successfully.", "vle_id": jsonReceived['vle_id']})
                except:
                    pass
            except:
                return Response({"Message":"Failed!", "Reason": "Some Error Occured. Please check your request body values!"})
        else:
            return Response({"Message": "Failed", "Reason": "Couldn't login! Try sending again!"})

class resetPassword(APIView):
    def post(self, request):
        jsonReceived = request.data
        if not 'vle_id' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "vle_id missing."})
        USERNAME = jsonReceived['utiuserid']
        PASSWORD = jsonReceived['utiuserpassword']
        if not USERNAME or not PASSWORD:
            return Response({"Message": "Failed!", "Reason": "Check your username and password!"})
        chrome_settings = webdriver.ChromeOptions()
        chrome_settings.add_argument('--headless')
        chrome_settings.add_argument('--no-sandbox')
        chrome_settings.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
        driver = webdriver.Chrome('pdfMergerAPI/chromedriver', options=chrome_settings)
        attempts = 0
        url = ''
        successFlag = 0
        while True:
            driver.get('https://www.psaonline.utiitsl.com/psaonline/showLogin')
            captcha = driver.find_element_by_xpath('//*[@id="PsaLoginAction"]/table/tbody/tr[8]/td/img')
            img_captcha_base64 = driver.execute_script("""
                                                        var ele = arguments[0];
                                                        var cnv = document.createElement('canvas');
                                                        cnv.width = ele.width; cnv.height = ele.height;
                                                        cnv.getContext('2d').drawImage(ele, 0, 0);
                                                        return cnv.toDataURL('image/png').substring(22);    
                                                        """, captcha)
            with open(r"captcha.png", 'wb') as f:
                f.write(base64.b64decode(img_captcha_base64))
            img = Image.open('captcha.png')
            captchaText = pytesseract.image_to_string(img)
            # print(captchaText)
            userField = driver.find_element_by_xpath('//*[@id="PsaLoginAction_userId"]')
            userField.send_keys(USERNAME)
            passField = driver.find_element_by_xpath('//*[@id="PsaLoginAction_password"]')
            passField.send_keys(PASSWORD)
            captchaField = driver.find_element_by_xpath('//*[@id="PsaLoginAction"]/table/tbody/tr[10]/td/input')
            captchaField.send_keys(captchaText)
            
            attempts += 1
            if driver.current_url == 'https://www.psaonline.utiitsl.com/psaonline/PsaLoginAction.action' or attempts>=10:
                if not attempts>=10:
                    successFlag = 1 
                break
            else:
                time.sleep(2)
            
        # time.sleep(2)
        if successFlag == 1:
            driver.get('https://www.psaonline.utiitsl.com/psaonline/resetvlepwd')
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="firstName"]').send_keys(jsonReceived['vle_id'])
            driver.find_element_by_xpath('//*[@id="Validate"]').click()
            time.sleep(2)
            try:
                if driver.find_element_by_xpath('//*[@id="dialog-message"]/p').text.strip() == "Password Changed Successfully...":
                    return Response({"Message": "Password Changed Successfully.", "vle_id": jsonReceived['vle_id']})
            except:
                pass
            return Response({"Message":"Failed!", "Reason": "Some Error Occured. Please check your vle_id!"})
        else:
            return Response({"Message": "Failed", "Reason": "Couldn't login! Try sending again!"})

class showItdQuery(APIView):
    def post(self, request):
        jsonReceived = request.data
        logging.info('REQUEST RECIVED')
        if not 'pan' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "vle_id missing."})
        if not 'utiuserid' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "utiuserid missing"})
        if not 'utiuserpassword' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "utiuserpassword missing"})
        USERNAME = jsonReceived['utiuserid']
        PASSWORD = jsonReceived['utiuserpassword']
        chrome_settings = webdriver.ChromeOptions()
        chrome_settings.add_argument('--headless')
        chrome_settings.add_argument('--no-sandbox')
        chrome_settings.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
        driver = webdriver.Chrome('pdfMergerAPI/chromedriver', options=chrome_settings)
        attempts = 0
        url = ''
        successFlag = 0
        while True:
            driver.get('https://www.psaonline.utiitsl.com/psaonline/showLogin')
            # time.sleep(2)
            logging.info('SOLVING', str(attempts+1))
            captcha = driver.find_element_by_xpath('//*[@id="PsaLoginAction"]/table/tbody/tr[8]/td/img')
            img_captcha_base64 = driver.execute_script("""
                                                        var ele = arguments[0];
                                                        var cnv = document.createElement('canvas');
                                                        cnv.width = ele.width; cnv.height = ele.height;
                                                        cnv.getContext('2d').drawImage(ele, 0, 0);
                                                        return cnv.toDataURL('image/png').substring(22);    
                                                        """, captcha)
            with open(r"captcha.png", 'wb') as f:
                f.write(base64.b64decode(img_captcha_base64))
            img = Image.open('captcha.png')
            captchaText = pytesseract.image_to_string(img)
            # thresh = 0
            # fn = lambda x : 255 if x > thresh else 0
            # img = img.convert('L').point(fn, mode='1')
            # img = ImageOps.invert(img)
            # img.save('captcha.png')
            # IMAGE_PATH = 'captcha.png'
            # reader = easyocr.Reader(['en'], model_storage_directory='/Users/akashweb/Downloads/english_g2.pth')
            # captchaText = reader.readtext(IMAGE_PATH,paragraph="False")[-1][-1]
            # with open('captchatext.txt', 'w+') as f:
            #     f.write(captchaText)
            userField = driver.find_element_by_xpath('//*[@id="PsaLoginAction_userId"]')
            userField.send_keys(USERNAME)
            passField = driver.find_element_by_xpath('//*[@id="PsaLoginAction_password"]')
            passField.send_keys(PASSWORD)
            captchaField = driver.find_element_by_css_selector('#PsaLoginAction > table > tbody > tr:nth-child(10) > td > input')
            captchaField.send_keys(captchaText)
            # driver.find_element_by_xpath('//*[@id="login"]').click()
            attempts += 1
            if driver.current_url == 'https://www.psaonline.utiitsl.com/psaonline/PsaLoginAction.action' or attempts>=10:
                if not attempts>=10:
                    successFlag = 1 
                break
            else:
                time.sleep(2)
            
        # time.sleep(2)
        if successFlag == 1:
            logging.info('LOGGED INTO PSA ONLINE')
            try:
                driver.get('https://www.psaonline.utiitsl.com/psaonline/showItdQuery')
                driver.find_element_by_xpath('//*[@id="selectedPan"]').send_keys(jsonReceived['pan'])
                driver.find_element_by_xpath('//*[@id="genRepo"]').click()
                time.sleep(1)
                resDict = {'pan_alloted_date': driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[3]/td[2]').text,
                            'pan_no': driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[4]/td[2]').text,
                            'applicants_first_name': driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[5]/td[2]').text,
                            'applicants_middle_name': driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[6]/td[2]').text,
                            'applicants_last_name': driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[7]/td[2]').text,
                            'fathers_first_name': driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[8]/td[2]').text,
                            'fathers_middle_name': driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[9]/td[2]').text,
                            'fathers_last_name': driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[10]/td[2]').text,
                            'gender': driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[11]/td[2]').text,
                            'area_code': str(driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[13]/td[2]').text).strip(),
                            'range_code': str(driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[13]/td[4]').text).strip(),
                            'ao_code': str(driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[13]/td[6]').text).strip(),
                            'ao_type': str(driver.find_element_by_xpath('//*[@id="challanForm"]/div/table/tbody/tr[13]/td[8]').text).strip(),
                            }
                return Response({"Message": "Success", "data": resDict})
            except:
                return Response({"Message": "Failed", "Message": "Invalid PAN"})
        else:
            return Response({"Message": "Failed", "Reason": "Couldn't login! Try sending again!"})
                                                      

class distributeCoupon(APIView):
    def post(self, request):
        jsonReceived = request.data
        if not 'vle_id' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "vle_id missing."})
        elif not 'no_of_with_card_coupons' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "no_of_with_card_coupons missing."})
        elif not 'no_of_without_card_coupons' in jsonReceived.keys():
            return Response({"Message": "Failed!", "Reason": "no_of_without_card_coupons missing."})
        USERNAME = jsonReceived['utiuserid']
        PASSWORD = jsonReceived['utiuserpassword']
        if not USERNAME or not PASSWORD:
            return Response({"Message": "Failed!", "Reason": "Check your username and password!"})
        chrome_settings = webdriver.ChromeOptions()
        chrome_settings.add_argument('--headless')
        chrome_settings.add_argument('--no-sandbox')
        chrome_settings.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
        driver = webdriver.Chrome('pdfMergerAPI/chromedriver', options=chrome_settings)
        attempts = 0
        url = ''
        successFlag = 0
        while True:
            driver.get('https://www.psaonline.utiitsl.com/psaonline/showLogin')
            captcha = driver.find_element_by_xpath('//*[@id="PsaLoginAction"]/table/tbody/tr[8]/td/img')
            img_captcha_base64 = driver.execute_script("""
                                                        var ele = arguments[0];
                                                        var cnv = document.createElement('canvas');
                                                        cnv.width = ele.width; cnv.height = ele.height;
                                                        cnv.getContext('2d').drawImage(ele, 0, 0);
                                                        return cnv.toDataURL('image/png').substring(22);    
                                                        """, captcha)
            with open(r"captcha.png", 'wb') as f:
                f.write(base64.b64decode(img_captcha_base64))
            img = Image.open('captcha.png')
            captchaText = pytesseract.image_to_string(img)
            # print(captchaText)
            userField = driver.find_element_by_xpath('//*[@id="PsaLoginAction_userId"]')
            userField.send_keys(USERNAME)
            passField = driver.find_element_by_xpath('//*[@id="PsaLoginAction_password"]')
            passField.send_keys(PASSWORD)
            captchaField = driver.find_element_by_xpath('//*[@id="PsaLoginAction"]/table/tbody/tr[10]/td/input')
            captchaField.send_keys(captchaText)
            
            attempts += 1
            if driver.current_url == 'https://www.psaonline.utiitsl.com/psaonline/PsaLoginAction.action' or attempts>=10:
                if not attempts>=10:
                    successFlag = 1 
                break
            else:
                time.sleep(2)
            
        # time.sleep(2)
        if successFlag == 1:
            try:
                driver.get('https://www.psaonline.utiitsl.com/psaonline/ScaCoupdistribution')
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="vleId"]').send_keys(jsonReceived['vle_id'])
                driver.find_element_by_xpath('//*[@id="noOfCoupons"]').send_keys(jsonReceived['no_of_with_card_coupons'])
                driver.find_element_by_xpath('//*[@id="myForm_noOfeCoupons"]').send_keys(jsonReceived['no_of_without_card_coupons'])
                driver.find_element_by_xpath('//*[@id="couponDis"]').click()
                time.sleep(2)
                try:
                    if driver.find_element_by_xpath('//*[@id="dialog-message"]/p').text.strip() == "Coupons are not available in your account as per the amount deposited. Your payment has not been recorded":
                        return Response({"Message": "Failed!", "Reason": "Coupons are not available in your account as per the amount deposited."})
                except:
                    pass
            except:
                return Response({"Message":"Failed!", "Reason": "Some Error Occured. Please check your vle_id!"})
            return Response({"Message": "Successful!"})
        else:
            return Response({"Message": "Failed", "Reason": "Couldn't login! Try sending again!"})

class pdfMergerAPI(APIView):

    def __init__(self):
        if os.path.exists('media'):
            shutil.rmtree('media/')
        os.makedirs('media/')

    def post(self, request):
        passwords = json.loads(request.POST['passwords'])
        filesDict = request.FILES
        files = []
        for k,v in filesDict.items():
            if re.match('^file*', k):
                files.append(v)
        # print(files)
        # exit(0)
        # strnames = [str(x) for x in files]
        BASE_PATH = 'media/'
        for file in files:
            with open(BASE_PATH + str(file), 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
        files = os.listdir(BASE_PATH)
        skippedFiles = []
        for file in files:
            if os.path.basename(file) in passwords.keys():
                password = passwords[os.path.basename(file)]
                try:
                    with pikepdf.open(BASE_PATH + file, password=password) as pdf:
                        pdf.save(BASE_PATH + file.replace('.pdf', '_decrypted.pdf'))
                        current_dir = os.getcwd()
                        # print(os.path.join(current_dir, BASE_PATH + file))
                        os.remove(os.path.join(current_dir, BASE_PATH + file))
                        pdf.close()
                except:
                    skippedFiles.append(os.path.basename(file))
        files = os.listdir(BASE_PATH)
        if request.POST['putSignature'] == 'True':
            # readableImage = []
            if len(files) !=2 or len(re.findall('.pdf', '|'.join(files))) != 1:
                return Response({'Status': 'Wrong type/number of files sent!', 'Number of files allowed': ['1 X pdf', '1 X jpg']}, status=status.HTTP_400_BAD_REQUEST)
            for file in files:
                if str(file).endswith('.pdf'):
                    imagesOfPdf = pdf2image.convert_from_bytes(open(BASE_PATH + file, 'rb').read())
                    # return Response({'data': imagesOfPdf}, status=status.HTTP_200_OK)
                    readableImage = np.array(imagesOfPdf[0])
                    cv2.imwrite(BASE_PATH+'base.jpg', cv2.cvtColor(readableImage, cv2.COLOR_RGB2BGR))
                else:
                    image = Image.open(BASE_PATH + file)
                    image.save(BASE_PATH + 'sign.png')
                os.remove(BASE_PATH + file)
            
            base = Image.open(BASE_PATH + 'base.jpg').convert('RGB')
            sign = cv2.imread(BASE_PATH + 'sign.png')
            img = cv2.imread(BASE_PATH + 'sign.png')
            alpha = 1.95 # Contrast control (1.0-3.0)
            beta = 0 # Brightness control (0-100)
            img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
            height, width, channel = img.shape
            if height > width:
                img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]
            mask = 255 - mask
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)
            mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)
            result = img.copy()
            result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
            result[:, :, 3] = mask
            cv2.imwrite(BASE_PATH+'sign.png', result)

            r, g, b = base.getpixel((500, 1070))
            background = Image.new('RGB', (400, 150), (r, g, b))
            # background = Image.new('RGB', (400, 150), (255, 255, 255))
            sign = Image.open(BASE_PATH + 'sign.png')
            sign = sign.resize((400,170))
            sign = sign.convert('RGBA')
            base.paste(background, (510,1090))
            base.paste(sign, (510,1090), mask=sign)
            # bottomBackground = Image.new('RGB', (220, 57), (255, 255, 255))
            # base.paste(bottomBackground, (382, 2125))
            sign = sign.resize((200, 40))
            base.paste(sign, (390, 2150), mask=sign)
            base.save(BASE_PATH + 'merged.png', format='png')
            base = Image.open(BASE_PATH + 'merged.png')
            pdf_bytes = img2pdf.convert(base.filename)
            file = open(BASE_PATH + 'merged.pdf', "wb")
            file.write(pdf_bytes)
            base.close()
            file.close()
            return FileResponse(open(BASE_PATH + 'merged.pdf', 'rb'))
        elif request.POST['putSignature'] == 'False':
            for file in files:
                if file.endswith(('.jpg', '.png', 'jpeg')):
                    # filesToBeMerged.remove(file)
                    imageName = file
                    image = Image.open(BASE_PATH + file)
                    pdf_bytes = img2pdf.convert(image.filename)
                    file = open(BASE_PATH + imageName.split('.')[0] + '.pdf', "wb")
                    file.write(pdf_bytes)
                    image.close()
                    file.close()
            try:
                files = sorted(glob.glob(BASE_PATH + '*.pdf'))
                merger = PdfMerger()
                for file in files:
                    merger.append(file)
                merger.write(BASE_PATH + 'merged.pdf')
                merger.close()
                return FileResponse(open(BASE_PATH + 'merged.pdf', 'rb'))
            except:
                return Response({'Status': 'PDF not Merged! Probable cause: Invalid Password List.'}, status=status.HTTP_200_OK)
        else:
            return Response({'Status': 'Invalid putSignature parameter!', 'Values allowed': ['True', 'False']}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({'Status': 'GET method not allowed!'}, status=status.HTTP_400_BAD_REQUEST)
        
