from selenium import webdriver
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time
import pandas as pd

#for testing time
start_time = time.time()

def vfcp_calc(input_filename,output_filename):

    # Define filepath
    filepath = 'input/'+input_filename+'.xlsx'
    # File to write to
    output_filepath = 'output/'+output_filename+'.xlsx'
    # Define VFCP Calculator website
    url = 'https://www.askebsa.dol.gov/VFCPCalculator/WebCalculator.aspx'
    
    # Import file
    df = pd.read_excel(filepath)
    
    # Split dates into individual columns for Month, Day, and Year
    df['Loss Month'] = df['Loss Date'].dt.month
    df['Loss Day'] = df['Loss Date'].dt.day
    df['Loss Year'] = df['Loss Date'].dt.year
    df['Recovery Month'] = df['Recovery Date'].dt.month
    df['Recovery  Day'] = df['Recovery Date'].dt.day
    df['Recovery Year'] = df['Recovery Date'].dt.year
    df['Final Payment Month'] = df['Final Payment Date'].dt.month
    df['Final Payment Day'] = df['Final Payment Date'].dt.day
    df['Final Payment Year'] = df['Final Payment Date'].dt.year
    
    #define form ids on website
    principalamt = '_ctl0_MainContent_txtPrincipal'
    lossmonth = '_ctl0_MainContent_txtLossDateMonth'
    lossday = '_ctl0_MainContent_txtLossDateDay'
    lossyear = '_ctl0_MainContent_txtLossDateYear'
    recovmonth = '_ctl0_MainContent_txtRecoveryDateMonth'
    recovday = '_ctl0_MainContent_txtRecoveryDateDay'
    recovyear ='_ctl0_MainContent_txtRecoveryDateYear'
    finalmonth = '_ctl0_MainContent_txtFinalPaymentMonth'
    finalday = '_ctl0_MainContent_txtFinalPaymentDay'
    finalyear = '_ctl0_MainContent_txtFinalPaymentYear'
    
    # Calculate and reset buttons
    calcbt = '_ctl0_MainContent_cmdCalculate'
    resetbt = '_ctl0_MainContent_cmdReset'
    
    # totals field to export to sheet
    totalsvalue = '_ctl0_MainContent_lblTotal'
    
    # Table with data
    #table = '_ctl0_MainContent_tblCalcData'
    
    data = [principalamt,lossmonth, lossday, lossyear, recovmonth,recovday, recovyear, finalmonth, finalday, finalyear]
    
    inputheaders = [
        df['Principal Amount'],
        df['Loss Month'],
        df['Loss Day'],
        df['Loss Year'],
        df['Recovery Month'],
        df['Recovery  Day'],
        df['Recovery Year'],
        df['Final Payment Month'],
        df['Final Payment Day'],
        df['Final Payment Year']
    ]
    
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()
    
    # Navigate to defined url
    driver.get(url)
    
    # Create list to log VFCP amounts
    vfcp = []
    
    # for each row
    for row in range(len(df)):
        for i in range(10):
            inputElement = driver.find_element_by_id(data[i])
            inputElement.send_keys(str(inputheaders[i][row]))
        driver.find_element_by_id(calcbt).click()
        dt = driver.find_element_by_id(totalsvalue)
        split = dt.text.split(": ")
        vfcp.append(split[1])
        driver.find_element_by_id(resetbt).click()
    
    driver.quit()
    
    #log amounts in new column
    df['VFCP Amt'] = vfcp
    
    # delete unnecessary headers
    del df['Loss Month']
    del df['Loss Day']
    del df['Loss Year']
    del df['Recovery Month']
    del df['Recovery  Day']
    del df['Recovery Year']
    del df['Final Payment Month']
    del df['Final Payment Day']
    del df['Final Payment Year']
    
    # Export File 
    writer = pd.ExcelWriter(output_filepath)
    # set index to false so that an addition column is not added
    df.to_excel(writer,'VFCP',index=False)
    writer.save()
    
    #for testing time
    totaltime = round((time.time() - start_time),2)
    print(len(df),"records reach in",totaltime," (",totaltime/len(df),"per record)")