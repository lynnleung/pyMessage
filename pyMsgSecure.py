import copy
import ctypes
import tkinter as tk
from ctypes import *
from tkinter import *
import numpy as np
import numpy.ctypeslib as npct

#声明需要调用的C函数
#from past.builtins import reduce

mylib_CRC = CDLL('\workspace\CRCcalcForPy.so')
mylib_Encry = CDLL('\\workspace\\xxtea.so')
#mylib_SEC =

#byte stable
header_init_byte = 'E9'
header_device_code = '00'
header_sequence_id = '00'
data_a_length_after_encode = '0000'
data_a_length_before_encode = '0000'
crc_data_a = ''
data_A_with_CRC = ''
message_hex = []
message_hex_int = []
data_A_message_1 = []
message_encry = []
message_to_print_to_encry = []
message_to_print_to_decode = []
total_message = [header_init_byte,
                 header_device_code,
                 data_a_length_after_encode,
                 data_a_length_before_encode,
                 data_A_message_1,
                 crc_data_a
                 ]
TEA_key = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10]

def get_hex_message_data_a():
    data_A_no_space = input_raw_data_A.get().replace(' ', '')
    # todo:对获取的数据做长度判断
    for i in range(len(data_A_no_space)):
        if i % 2 == 0:
            k = i / 2
            str_temp = data_A_no_space[i] + data_A_no_space[i + 1]
            data_A_message_1.append(str_temp)

    for i in range(len(data_A_message_1)):
        temp = '0x' + data_A_message_1[i]
        # change to int is OK
        temp1 = int(temp, base=16)
        message_hex.append(temp1)

def test_get_hex_message_data_a():
    data_A_no_space = input_raw_data_A.get().replace(' ', '')
    for i in range(len(data_A_no_space)):
        temp_data_a = data_A_no_space[i]
        if temp_data_a == 'a' or temp_data_a == 'A':
            message_hex.append(10)
        elif temp_data_a == 'b' or temp_data_a == 'B':
            message_hex.append(11)
        elif temp_data_a == 'c' or temp_data_a == 'C':
            message_hex.append(12)
        elif temp_data_a == 'd' or temp_data_a == 'D':
            message_hex.append(13)
        elif temp_data_a == 'e' or temp_data_a == 'E':
            message_hex.append(14)
        elif temp_data_a == 'f' or temp_data_a == 'F':
            message_hex.append(15)
        else:
            message_hex.append(temp_data_a)

#todo:function to accepct int message,output hex message
def cal_int_to_hex_msg(raw_message):
    temp_raw_message = copy.deepcopy(raw_message)
    for i in range(len(temp_raw_message)):
        temp1 = hex(temp_raw_message[i])
        temp2 = '{:02x}'.format(temp_raw_message[i])
        #get the hex to verify encode
        message_hex_int.append(temp2)
    message_encry = copy.deepcopy(message_hex_int)
    print(message_hex_int)

#calculate secure message of data A
def secure_cal():
    message_hex.clear()
    #获取定义的message_hex消息
    test_get_hex_message_data_a()
    # 声明一个数组指针，并为之申请一段空间
    input_c_used_msg_hex = c_char * (len(message_hex)*4)
    # 将该指针实例化
    input_c_sample = input_c_used_msg_hex()
    for i in range(len(message_hex)):
        #ctypes 支持的格式是bytes,因此将消息中的int类型转换为bytes
        test_input_bytes = message_hex[i].to_bytes(1,byteorder='big')
        input_c_sample[i] = test_input_bytes

    size_of_data_a = 4*len(message_hex)
    size_of_key = len(TEA_key)
    #将秘钥转换为ctypes可以支持的类型
    ctype_tea_keys = (ctypes.c_char * size_of_key)(*TEA_key)

    #声明将要调用的函数
    cfunc_encode_msg = mylib_Encry.encryptXXTEA
    cfunc_encode_msg(input_c_sample, ctypes.c_int(size_of_data_a), ctype_tea_keys)
    for i in range(len(input_c_sample)):
        #将加密后的byte类型转换为hex string并打印到entry窗口
        message_to_print_to_encry.append(bytesToHexString(input_c_sample[i]))
        secure_data_a_result.insert(i*2,message_to_print_to_encry[i])
'''
# 声明将要调用的函数
    cfunc_decode_msg = mylib_Encry.decrpytXXTEA
#    cfunc_decode_msg(test_c_sample_de, ctypes.c_int(size_of_data_a), ctype_tea_keys)
    cfunc_decode_msg(input_c_sample, ctypes.c_int(size_of_data_a), ctype_tea_keys)
#    cfunc_decode_msg(test_c_sample_de_1, ctypes.c_int(size_of_data_a), ctype_tea_keys)
    for i in range(len(input_c_sample.value)):
        temp_input = input_c_sample.value[i]
        temp_print = ''
        if temp_input == 10:
            temp_print = 'A'
        elif temp_input == 11:
            temp_print = 'B'
        elif temp_input == 12:
            temp_print = 'C'
        elif temp_input == 13:
            temp_print = 'D'
        elif temp_input == 14:
            temp_print = 'E'
        elif temp_input == 15:
            temp_print = 'F'
        else:
            temp_print = temp_input
        decode_data_a_result.insert(i,temp_print)
#    print(message_hex)
'''
def cal_total_message():
    get_hex_message_data_a()
    crc_data_a = CRC_calculation(message_hex)
    #todo:combine the message
    total_msg_with_CRC_result.insert(0,total_message)

def decode_cal():
    # 获取定义的message_hex消息
    message_hex.clear()
    get_hex_message_data_a()
    # 声明一个数组指针，并为之申请一段空间
    de_input_c_used_msg_hex = c_char * len(message_hex)
    # 将该指针实例化
    de_input_c_sample = de_input_c_used_msg_hex()
    for i in range(len(message_hex)):
        # ctypes 支持的格式是bytes,因此将消息中的int类型转换为bytes
        de_input_c_sample[i] = message_hex[i]
    size_of_data_a = len(message_hex)
    size_of_key = len(TEA_key)
    # 将秘钥转换为ctypes可以支持的类型
    ctype_tea_keys = (ctypes.c_char * size_of_key)(*TEA_key)
    # 声明将要调用的函数
    cfunc_decode_msg = mylib_Encry.decrpytXXTEA
    cfunc_decode_msg(de_input_c_sample, ctypes.c_int(size_of_data_a), ctype_tea_keys)
    for i in range(len(de_input_c_sample.value)):
        temp_input = de_input_c_sample.value[i]
        temp_dec_print = ''
        if temp_input == 10:
            temp_dec_print = 'A'
        elif temp_input == 11:
            temp_dec_print = 'B'
        elif temp_input == 12:
            temp_dec_print = 'C'
        elif temp_input == 13:
            temp_dec_print = 'D'
        elif temp_input == 14:
            temp_dec_print = 'E'
        elif temp_input == 15:
            temp_dec_print = 'F'
        else:
            temp_dec_print = temp_input
        decode_data_a_result.insert(i, temp_dec_print)
#    print(message_hex)

def CRC_calculation(message_data):
    #申明所需要调用的扩展C函数
    CRCcalc = mylib_CRC.calc_CRC
    #测试数据，之后将所获取到的数据转换为此类数据
#   message_data = [0xE9,0x00,0x00,0X0D,0X00,0X13,0X01,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0X03,0XFF,0XFF,0X00]
    sizeOfData = len(message_data)
    ctype_message_data = (ctypes.c_char*sizeOfData)(*message_data)

    crc_result_string = CRCcalc(ctype_message_data, ctypes.c_int(sizeOfData))
    return crc_result_string
    print("crc is:", crc_result_string)
def bytesToHexString(bs):
    # hex_str = ''
    # for item in bs:
    #     hex_str += str(hex(item))[2:].zfill(2).upper() + " "
    # return hex_str
    return ''.join(['%02X ' % b for b in bs])
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
#button-encode data a
secure_data_a_label = Label(window, text='Cal encryp of Data A')
secure_data_a_label.place(x=20, y=50)
secure_data_a_button=Button(window,text='EncrypData',bg='lightblue',width=20,command=secure_cal)
secure_data_a_button.place(x=150,y=50)
secure_data_a_result_text = StringVar(value='')
secure_data_a_result=Entry(window,textvariable=secure_data_a_result_text,width=80)
secure_data_a_result.place(x=20,y=70)
#button-calculate the CRC and combine all the message
total_msg_with_CRC_label = Label(window, text='Total msg with CRC')
total_msg_with_CRC_label.place(x=20, y=90)
total_msg_with_CRC_button=Button(window,text='cal total msg',bg='lightblue',width=20,command=cal_total_message)
total_msg_with_CRC_button.place(x=150,y=90)
total_msg_with_CRC_result_text = StringVar(value='')
total_msg_with_CRC_result=Entry(window,textvariable=total_message,width=100)
total_msg_with_CRC_result.place(x=20,y=110)
#BUTTON-decode data a
decode_data_a_label = Label(window, text='Cal decode of Data A')
decode_data_a_label.place(x=20, y=130)
decode_data_a_button=Button(window,text='Decode',bg='lightblue',width=20,command=decode_cal)
decode_data_a_button.place(x=150,y=130)
decode_data_a_result_text = StringVar(value='')
decode_data_a_result=Entry(window,textvariable=decode_cal(),width=80)
decode_data_a_result.place(x=20,y=150)

window.mainloop()