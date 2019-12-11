from ctypes import *
from tkinter import *
from tkinter.ttk import Combobox
import ctypes
import binascii

#声明需要调用的C函数
#from past.builtins import reduce

mylib = CDLL('\workspace\CRCcalcForPy.so')

#声明消息集合
msgID = ['0x01_network_control',
         '0x11_device_info'
         '0x12_running_data',
         '0x13_configure_info',
         '0x14_timing_info']
msgType = ['0x01_report',
           '0x02_change',
           '0x03_query']
msgIdWifiEnroll=['0x00_No_enroll_request',
                 '0x01_request_for_BLE_enroll',
                 '0x02_request_softAP_enroll',
                 '0x0F_request_for_unenroll_from_current_wifi_net',
                 '0xFE_enroll_finished',
                 '0xFF_Uninitialized_for_wifi',
                 '0xFF_no_change_for_device']
msgIdWifiStatus=['0x00_No_wifi_config',
                 '0x01_no_wifi_netw_signal',
                 '0x02_wifi_connected',
                 '0x03_in_BLE_mode',
                 '0x04_in_softAP_mode',
                 '0xFF_Uninitialized']
msgIdSignalStren=['0x01', '0x02', '0x03', '0x04', '0x05', '0x06', '0x07', '0x08', '0x09', '0xFF']



#定义此类用于计算帧长度，并显示帧长度，这是因为帧长度为2byte
class msgByteStruc():
    byteLength=0
    byteValue=0
    byte_list = []
    def get_msg_value(self):
        return self.byteValue

    def get_msg_length(self):
        return self.byteLength

    def set_msg_value(self,valueInt):
        self.byteValue = valueInt

    def get_hex_msg(self):
        if self.byteLength == 0:
            return ''
        elif self.byteLength == 1:
            self.byte_list.append(format(self.byteValue,'02x'))
            return self.byte_list
        elif self.byteLength == 2:
            self.byte_list.append(format(0,'02x'))
            self.byte_list.append(format(self.byteValue,'02x'))
            return self.byte_list
        else:
            raise ValueError('byte length is larger than 2!')

class MY_GUI(Frame):
#构造函数
    def __init__(self,name):
        self.init_window_name=name
    #窗口控件设置初始化
    def set_init_window(self):
        self.init_window_name.title('消息组合')
        self.init_window_name.geometry('1168x631+20+10')
        self.init_window_name['bg']='grey'
        self.init_window_name.attributes('-alpha',1)

        #标签：header 起始位：1byte；0XE9
        self.label_init_1_byte = Label(self.init_window_name,text='起始位')
        self.label_init_1_byte.place(x=30,y=30)
        self.header_init_byte = 'E9'
        self.input_init_1_byte_value = StringVar(value=self.header_init_byte)
        self.input_init_1_byte = Entry(self.init_window_name, textvariable=self.input_init_1_byte_value, width=8)
        self.input_init_1_byte.place(x=30, y=60)
        self.input_init_length=1

        # 标签：header 设备码：1byte；0X00
        self.label_deviceId_1_byte = Label(self.init_window_name, text='设备码')
        self.label_deviceId_1_byte.place(x=80, y=30)
        self.header_device_code = '00'
        self.input_deviceId_1_byte_value = StringVar(value=self.header_device_code)
        self.input_deviceId_1_byte = Entry(self.init_window_name, textvariable=self.input_deviceId_1_byte_value, width=8)
        self.input_deviceId_1_byte.place(x=80, y=60)
        self.deviceId_length = 1

        # header 帧长度：2 bytes；
        self.label_length_2_bytes = Label(self.init_window_name, text='帧长度')
        self.label_length_2_bytes.place(x=130, y=30)
        self.header_frame_length = ''
        self.input_length_2_bytes_value = StringVar(value=self.header_frame_length)
        self.input_length_2_bytes = Entry(self.init_window_name, textvariable=self.input_length_2_bytes_value, width=8)
        self.input_length_2_bytes.place(x=130, y=60)
        self.list_seqLength = []


        # header 序列号：1 bytes；
        self.label_seq_1_bytes = Label(self.init_window_name, text='序列号')
        self.label_seq_1_bytes.place(x=180, y=30)
        self.header_sequence_id = '00'
        self.label_seq_1_bytes_value = StringVar(value='00')
        self.input_seq_1_bytes = Entry(self.init_window_name, textvariable=self.label_seq_1_bytes_value, width=8)
        self.input_seq_1_bytes.place(x=180, y=60)
        self.input_seq_length = 1
        self.seqLength = msgByteStruc()
        self.seqLength.byteLength = 2

        # Network control:message id;data A area
        # message id: 0x01 network control;0x11 device info;0x12 running data;0x13 config info;
        # 提供一个选择框，选择添加的消息类型
        # 给选择框加上label
        self.message_id_choose_label = Label(self.init_window_name, text='message id')
        self.message_id_choose_label.place(x=250, y=30)
        self.message_id_value = StringVar(value=msgID[0])
        self.message_id_choose_combo = Combobox(self.init_window_name, width=30, textvariable=self.message_id_value)
        self.message_id_choose_combo['values'] = msgID
        self.message_id_raw_value = self.message_id_choose_combo.get()[2:4]
        self.message_id_choose_combo.bind("<<ComboboxSelected>>", self.msg_id_choose)
        self.message_id_choose_combo['state'] = 'readonly'
        self.message_id_choose_combo.grid(row=200, column=200, padx=250, pady=60)

        # Network control:message type
        # 针对每一条消息添加一个框架
        #message id
        self.message_id_frame = Frame(self.init_window_name)
        self.message_id_frame.place(x=30, y=100)
        self.message_id_frame_label = Label(self.message_id_frame,text='Network Control 0x01')
        self.message_id_frame_label.grid(row=0,column=0,sticky=W)
        #message type
        self.message_id_frame_type_label = Label(self.message_id_frame,text='message type')
        self.message_id_frame_type_label.grid(row=5,column=0,sticky=W)
        self.message_id_frame_type_text = StringVar(value=msgType[0])
        self.message_id_frame_type_combo = Combobox(self.message_id_frame,width=10, textvariable=self.message_id_frame_type_text)
        self.message_id_frame_type_combo['values'] = msgType
        self.message_id_frame_type_combo.grid(row=10,column=0,padx=0,pady=20)
        self.msg_type_value = self.message_id_frame_type_combo.get()[2:4]
        self.message_id_frame_type_combo.bind("<<ComboboxSelected>>", self.msg_type)

        #wifi enroll
        self.message_id_frame_wifi_enroll_label = Label(self.message_id_frame, text='Wifi enroll')
        self.message_id_frame_wifi_enroll_label.grid(row=5, column=10, sticky=W)
        self.message_id_frame_wifi_enroll_text = StringVar(value=msgIdWifiEnroll[0])
        self.message_id_frame_wifi_enroll_combo = Combobox(self.message_id_frame, width=30,
                                                    textvariable=self.message_id_frame_wifi_enroll_text)
        self.message_id_frame_wifi_enroll_combo['values'] = msgIdWifiEnroll
        self.message_id_frame_wifi_enroll_combo.grid(row=10, column=10, padx=0, pady=20)
        self.netctrl_wifi_enroll_value = self.message_id_frame_wifi_enroll_combo.get()[2:4]
        self.message_id_frame_wifi_enroll_combo.bind("<<ComboboxSelected>>", self.msg_NETCTRL_wifi_enroll_status)

        #wifi status
        self.message_id_frame_wifi_status_label = Label(self.message_id_frame, text='Wifi status')
        self.message_id_frame_wifi_status_label.grid(row=5, column=20, sticky=W)
        self.message_id_frame_wifi_status_text = StringVar(value=msgIdWifiStatus[0])
        self.message_id_frame_wifi_status_combo = Combobox(self.message_id_frame, width=20,
                                                           textvariable=self.message_id_frame_wifi_status_text)
        self.message_id_frame_wifi_status_combo['values'] = msgIdWifiStatus
        self.message_id_frame_wifi_status_combo.grid(row=10, column=20, padx=0, pady=20)
        self.netctrl_wifi_status_value= self.message_id_frame_wifi_status_combo.get()[2:4]
        self.message_id_frame_wifi_status_combo.bind("<<ComboboxSelected>>", self.msg_NETCTRL_wifi_status)

        #mac address
        #input box
        self.message_id_frame_macAddr_label = Label(self.message_id_frame,text='MAC Address')
        self.message_id_frame_macAddr_label.grid(row=5,column=30,sticky=W)
        self.netctrl_MAC_addr_1 ='00'
        self.netctrl_MAC_addr_2 ='FF'
        self.message_id_frame_macAddr_text = StringVar(value=self.netctrl_MAC_addr_1+self.netctrl_MAC_addr_2)
        self.message_id_frame_macAddr_entry = Entry(self.message_id_frame, textvariable=self.message_id_frame_macAddr_text, width=8)
        self.mac_address_input = ''
        self.message_id_frame_macAddr_entry.grid(row=10, column=30, padx=0, pady=8)
        #signal strength
        self.message_id_frame_signalStren_label = Label(self.message_id_frame,text='Signal Strength')
        self.message_id_frame_signalStren_label.grid(row=5,column=40,sticky=W)
        self.message_id_frame_signalStren_text = StringVar(value=msgIdSignalStren[0])
        self.message_id_frame_signalStren_combo = Combobox(self.message_id_frame,width=5,textvariable=self.message_id_frame_signalStren_text)
        self.message_id_frame_signalStren_combo['values'] = msgIdSignalStren
        self.netctrl_signal_stren = self.message_id_frame_signalStren_combo.get()[2:4]
        self.message_id_frame_signalStren_combo.grid(row=10,column=40,padx=0,pady=5)
        self.message_id_frame_signalStren_combo.bind("<<ComboboxSelected>>", self.msg_id_signal_stren_choose)
        #reserved byte
        self.message_id_frame_reserved_label = Label(self.message_id_frame, text='Reserved')
        self.message_id_frame_reserved_label.grid(row=5, column=50, sticky=W)
        self.netctrl_reserved = '00'
        self.message_id_frame_reserved_text = StringVar(value=self.netctrl_reserved)
        self.message_id_frame_reserved_entry = Entry(self.message_id_frame,
                                                    textvariable=self.message_id_frame_reserved_text, width=8)
        self.message_id_frame_reserved_entry.grid(row=10, column=50, padx=0, pady=8)

        #CRC calculate
        #press button to trigger
        self.message_id_frame_CRC_label = Label(self.message_id_frame,text='CRC calculate')
        self.message_id_frame_CRC_label.grid(row=5,column=60,sticky=W)
        self.message_id_frame_CRC_button=Button(self.message_id_frame,text='计算',bg='lightblue',width=6,command=self.calculation_raw_message_network_control)
        self.message_id_frame_CRC_button.grid(row=10, column=60)
        self.message_id_frame_CRC_result_text = StringVar(value='')
        self.message_id_frame_CRC_result=Entry(self.message_id_frame,textvariable=self.message_id_frame_CRC_result_text,width=8)
        self.message_id_frame_CRC_result.grid(row=10,column=68,padx=0,pady=8)

        #raw message
        self.message_id_frame_raw_message_label = Label(self.message_id_frame,text='raw message')
        self.message_id_frame_raw_message_label.grid(row=5,column=70,sticky=W)
        self.message_id_frame_raw_message_text=StringVar(value='')
        self.message_id_frame_raw_message = Entry(self.message_id_frame,textvariable=self.calculation_raw_message_network_control,width=80)
        self.message_id_frame_raw_message.grid(row=10,column=70,padx=0,pady=80)


        #Device information
        self.device_info_frame = Frame(self.init_window_name)
        self.device_info_frame.place(x=30,y=200)
        self.device_info_frame_label = Label(self.device_info_frame, text='Device information 0x11')
        self.device_info_frame_label.grid(row=0,column=0,sticky=W)
        #message type
        self.device_info_msg_type_label = Label(self.message_id_frame, text='message type')
        self.device_info_msg_type_label.grid(row=5, column=0, sticky=W)
        self.device_info_msg_type_text = StringVar(value=msgType[0])
        self.device_info_msg_type_combo = Combobox(self.message_id_frame, width=10,
                                                    textvariable=self.message_id_frame_type_text)
        self.device_info_msg_type_combo['values'] = msgType
        self.device_info_msg_type_combo.grid(row=10, column=0, padx=0, pady=20)
        self.device_info_msg_type_value = self.device_info_msg_type_combo.get()[2:4]
        self.device_info_msg_type_combo.bind("<<ComboboxSelected>>", self.msg_type)















        #frame 3:running data
        self.running_data_frame = Frame(self.init_window_name)
        self.running_data_frame.place(x=30,y=300)
        #frame 4:config info
        self.config_info_frame = Frame(self.init_window_name)
        self.config_info_frame.place(x=30,y=400)
        #根据消息选择框的选择，选择消息

    #调用C函数计算消息的CRC
    #input data type can be int
    def CRC_calculation(self, message_data):
        #申明所需要调用的扩展C函数
        CRCcalc = mylib.calc_CRC
        #测试数据，之后将所获取到的数据转换为此类数据
#        message_data = [0xE9,0x00,0x00,0X0D,0X00,0X13,0X01,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0X03,0XFF,0XFF,0X00]
        sizeOfData = len(message_data)
        ctype_message_data = (ctypes.c_char*sizeOfData)(*message_data)

        crc_result_string = CRCcalc(ctype_message_data, ctypes.c_int(sizeOfData))
        if self.message_id_frame_CRC_result.get() != '':
            self.message_id_frame_CRC_result.delete(0,END)
        self.message_id_frame_CRC_result.insert(0,hex(crc_result_string))
        crc_result_string_hex = hex(crc_result_string)[2:]

        return crc_result_string_hex
        print("crc is:", crc_result_string)

    #计算raw message
    def calculation_raw_message_network_control(self):
        #network control消息URAT发出的支持：change;query;
        #when the message type is query, the data length of data A should be 2 and
        #no CRC
        #当消息类型是report的时候，报所有
        self.message_address_input = self.message_id_frame_macAddr_entry.get()
        self.netctrl_MAC_addr_1 = self.message_address_input[0:2]
        self.netctrl_MAC_addr_2 = self.message_address_input[2:4]
        if self.msg_type_value == '02':
            self.network_control_raw_message_dataA = [self.message_id_raw_value,
                                                  self.msg_type_value,
                                                  self.netctrl_wifi_enroll_value,
                                                  self.netctrl_wifi_status_value,
                                                  self.netctrl_MAC_addr_1,
                                                  self.netctrl_MAC_addr_2,
                                                  self.netctrl_signal_stren,
                                                  self.netctrl_reserved
                                                  ]
            self.header_frame_length = len(self.network_control_raw_message_dataA)
            self.frame_length_list = self.frame_length_get_hex_msg(self.header_frame_length,2)
            self.netctrl_crc_message = [self.header_device_code,
                                    self.frame_length_list[0],
                                    self.frame_length_list[1],
                                    self.header_sequence_id,
                                    self.message_id_raw_value,
                                    self.msg_type_value,
                                    self.netctrl_wifi_enroll_value,
                                    self.netctrl_wifi_status_value,
                                    self.netctrl_MAC_addr_1,
                                    self.netctrl_MAC_addr_2,
                                    self.netctrl_signal_stren,
                                    self.netctrl_reserved
                                    ]
            self.netctrl_crc_message_hex = []
            for i in range(len(self.netctrl_crc_message)):
                temp = '0x'+self.netctrl_crc_message[i]
                #change to int is OK
                temp1 = int(temp, base=16)
                self.netctrl_crc_message_hex.append(temp1)
            self.crc_result_string = ''
            self.crc_result_string = self.CRC_calculation(self.netctrl_crc_message_hex)
            self.netctrl_raw_message_with_crc = [self.header_init_byte,
                                             self.header_device_code,
                                             self.frame_length_list[0],
                                             self.frame_length_list[1],
                                             self.header_sequence_id,
                                             self.message_id_raw_value,
                                             self.msg_type_value,
                                             self.netctrl_wifi_enroll_value,
                                             self.netctrl_wifi_status_value,
                                             self.netctrl_MAC_addr_1,
                                             self.netctrl_MAC_addr_2,
                                             self.netctrl_signal_stren,
                                             self.netctrl_reserved,
                                             self.crc_result_string
                                        ]
            #print(self.netctrl_crc_message_hex)
            #print(self.netctrl_raw_message_with_crc)

            self.input_length_2_bytes.delete(0,END)
            self.input_length_2_bytes.insert(0,self.header_frame_length)
            self.message_id_frame_raw_message.delete(0, END)
            for i in range(len(self.netctrl_raw_message_with_crc)):
                self.message_id_frame_raw_message.insert(i*2,self.netctrl_raw_message_with_crc[i])
        elif self.msg_type_value == '03':
            self.network_control_raw_message_dataA = [self.message_id_raw_value,
                                                      self.msg_type_value
                                                      ]
            self.header_frame_length = len(self.network_control_raw_message_dataA)
            self.frame_length_list = self.frame_length_get_hex_msg(self.header_frame_length, 2)
            self.netctrl_crc_message = [self.header_device_code,
                                        self.frame_length_list[0],
                                        self.frame_length_list[1],
                                        self.header_sequence_id,
                                        self.message_id_raw_value,
                                        self.msg_type_value
                                        ]
            self.netctrl_crc_message_hex = []
            for i in range(len(self.netctrl_crc_message)):
                temp = '0x' + self.netctrl_crc_message[i]
                # change to int is OK
                temp1 = int(temp, base=16)
                self.netctrl_crc_message_hex.append(temp1)
            self.crc_result_string = ''
            self.crc_result_string = self.CRC_calculation(self.netctrl_crc_message_hex)
            self.netctrl_raw_message_with_crc = [self.header_init_byte,
                                                 self.header_device_code,
                                                 self.frame_length_list[0],
                                                 self.frame_length_list[1],
                                                 self.header_sequence_id,
                                                 self.message_id_raw_value,
                                                 self.msg_type_value,
                                                 self.crc_result_string
                                                 ]
            self.input_length_2_bytes.delete(0, END)
            self.input_length_2_bytes.insert(0, self.header_frame_length)

            self.message_id_frame_raw_message.delete(0,END)
            for i in range(len(self.netctrl_raw_message_with_crc)):
                self.message_id_frame_raw_message.insert(i * 2, self.netctrl_raw_message_with_crc[i])
        elif self.msg_type_value == '01':
            self.message_id_frame_raw_message.delete(0, END)
            self.message_id_frame_raw_message.insert(0,"Network control message do not support report type!")
        else:
            raise ValueError("Error message type!")


    def msg_id_choose(self, *args):
#        print(self.message_id_raw_value)
        msg_id_choose_string = self.message_id_choose_combo.get()
#        print(msg_id_choose_string)
        if msgID.index(msg_id_choose_string) >= 0 & msgID.index(msg_id_choose_string) <= len(msgID):
            position_msg_id_choose = msgID.index(msg_id_choose_string)
            self.message_id_raw_value = msgID[position_msg_id_choose][2:4]
        else:
            raise ValueError("the message id is error!")
#        print(self.message_id_raw_value)

    def msg_type(self, *args):

        msg_type_string = self.message_id_frame_type_combo.get()
#        print(msg_type_string)
        if msgType.index(msg_type_string) >= 0 & msgType.index(msg_type_string) <= len(msgType):
            position_value_msg_type = msgType.index(msg_type_string)
            self.msg_type_value = msgType[position_value_msg_type][2:4]
        else:
            raise ValueError('The message type is error!')
#        print(self.msg_type_value)

    def msg_NETCTRL_wifi_enroll_status(self, *args):

        msg_wifi_enroll_string = self.message_id_frame_wifi_enroll_combo.get()
#        print(msg_wifi_enroll_string)
        if msgIdWifiEnroll.index(msg_wifi_enroll_string) >= 0 & msgIdWifiEnroll.index(msg_wifi_enroll_string) <= len(msgIdWifiEnroll):
            position_value = msgIdWifiEnroll.index(msg_wifi_enroll_string)
            self.netctrl_wifi_enroll_value = msgIdWifiEnroll[position_value][2:4]
        else:
            raise ValueError("message id wifi enroll string is error!")
#       print(self.msg_wifi_enroll_value)

    def msg_NETCTRL_wifi_status(self, *args):
#        print(self.msg_wifi_status_value)
        msg_wifi_status_string = self.message_id_frame_wifi_status_combo.get()
        print(msg_wifi_status_string)
        if msgIdWifiStatus.index(msg_wifi_status_string) >= 0 & msgIdWifiStatus.index(msg_wifi_status_string) <= len(msgIdWifiEnroll):
            position_value_wifi_status = msgIdWifiStatus.index(msg_wifi_status_string)
            self.netctrl_wifi_status_value = msgIdWifiStatus[position_value_wifi_status][2:4]
        else:
            raise ValueError("message id wifi status is error!")
#        print(self.msg_wifi_status_value)
    def msg_id_signal_stren_choose(self, *args):
        msg_wifi_signal_stren = self.message_id_frame_signalStren_combo.get()
#        print(msg_wifi_signal_stren)
        if msgIdSignalStren.index(msg_wifi_signal_stren)>=0 & msgIdSignalStren.index(msg_wifi_signal_stren)<=len(msgIdSignalStren):
            position_wifi_signal_stren = msgIdSignalStren.index(msg_wifi_signal_stren)
            self.netctrl_signal_stren = msgIdSignalStren[position_wifi_signal_stren][2:4]
        else:
            raise ValueError("network control wifi signal strength is wrong!")
#        print(self.netctrl_signal_stren)

    def frame_length_get_hex_msg(self,frameLengthData, byteLength):
        frameLengthDataList = []
        if byteLength == 0:
            raise ValueError('frame length can not be 0')
        elif byteLength == 1:
            frameLengthDataList.append(format(frameLengthData,'02x'))
            return frameLengthDataList
        elif byteLength == 2:
            frameLengthDataList.append(format(0,'02x'))
            frameLengthDataList.append(format(frameLengthData,'02x'))
            return frameLengthDataList
        else:
            raise ValueError('byte length is larger than 2!')

    def return_mac_address_input(self, *args):
        mac_address_input_string = self.message_id_frame_macAddr_entry.get()
        self.netctrl_MAC_addr_1 = mac_address_input_string[0:1]
        self.netctrl_MAC_addr_2 = mac_address_input_string[2:3]

#主线程
if __name__ == '__main__':
    init_window=Tk()
    window = MY_GUI(init_window)
    window.set_init_window()
#    window.pack()
    init_window.mainloop()
