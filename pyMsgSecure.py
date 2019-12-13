from ctypes import *
import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
import ctypes
import binascii

#声明需要调用的C函数
#from past.builtins import reduce

mylib_CRC = CDLL('\workspace\CRCcalcForPy.so')
#mylib_SEC =

#byte stable
header_init_byte = 'E9'
header_device_code = '00'
frame_length_before_sec = ''
frame_length_after_sec = ''
header_sequence_id = '00'
data_A_with_CRC = ''
message_hex = []
data_A_message_1 = []

#calculate secure message of data A
def secure_cal():
    pass

def cal_total_message():

    data_A_no_space = input_raw_data_A.get().replace(' ','')
    #todo:对获取的数据做长度判断
    for i in range(len(data_A_no_space)):
        if i%2 == 0:
            k=i/2
            str_temp = data_A_no_space[i]+data_A_no_space[i+1]
            data_A_message_1.append(str_temp)

    for i in range(len(data_A_message_1)):
        temp = '0x' + data_A_message_1[i]
        # change to int is OK
        temp1 = int(temp, base=16)
        message_hex.append(temp1)
    crc_data_a = CRC_calculation(message_hex)
    data_A_with_CRC = crc_data_a
    return crc_data_a
#    pass

def decode_cal():
    pass

def CRC_calculation(message_data):
    #申明所需要调用的扩展C函数
    CRCcalc = mylib_CRC.calc_CRC
    #测试数据，之后将所获取到的数据转换为此类数据
#       message_data = [0xE9,0x00,0x00,0X0D,0X00,0X13,0X01,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0X03,0XFF,0XFF,0X00]
    sizeOfData = len(message_data)
    ctype_message_data = (ctypes.c_char*sizeOfData)(*message_data)

    crc_result_string = CRCcalc(ctype_message_data, ctypes.c_int(sizeOfData))
    return crc_result_string
    print("crc is:", crc_result_string)



#frame
window = tk.Tk()
window.title('message secure')
window.geometry('600x400')
tk.Label(window,text='Data A secure tool').pack()
#input raw data A entry
frm = tk.Frame(window)
label_raw_data_A = Label(window, text='Please input raw data')
label_raw_data_A.place(x=20,y=10)
input_raw_data = ''
input_raw_data_A = Entry(window,textvariable=input_raw_data,width=80)
input_raw_data_A.place(x=20,y=30)
data_A_message = input_raw_data_A.get()

#button-secure
secure_data_a_label = Label(window, text='Cal encryp of Data A')
secure_data_a_label.place(x=20, y=50)
secure_data_a_button=Button(window,text='EncrypData',bg='lightblue',width=20,command=secure_cal)
secure_data_a_button.place(x=150,y=50)
secure_data_a_result_text = StringVar(value='')
secure_data_a_result=Entry(window,textvariable=secure_cal(),width=80)
secure_data_a_result.place(x=20,y=70)
#button-CRC
total_msg_with_CRC_label = Label(window, text='Total msg with CRC')
total_msg_with_CRC_label.place(x=20, y=90)
total_msg_with_CRC_button=Button(window,text='cal total msg',bg='lightblue',width=20,command=cal_total_message)
total_msg_with_CRC_button.place(x=150,y=90)
total_msg_with_CRC_result_text = StringVar(value='')
total_msg_with_CRC_result=Entry(window,textvariable=data_A_with_CRC,width=100)
total_msg_with_CRC_result.place(x=20,y=110)
#BUTTON-UNSECURE
decode_data_a_label = Label(window, text='Cal decode of Data A')
decode_data_a_label.place(x=20, y=130)
decode_data_a_button=Button(window,text='Decode',bg='lightblue',width=20,command=secure_cal)
decode_data_a_button.place(x=150,y=130)
decode_data_a_result_text = StringVar(value='')
decode_data_a_result=Entry(window,textvariable=decode_cal(),width=80)
decode_data_a_result.place(x=20,y=150)

window.mainloop()