#include<stdio.h>

typedef unsigned char   FLAG;       /* boolean data */
typedef unsigned char   U8BIT;      /* unsigned 8 bit data */
typedef unsigned short  U16BIT;     /* unsigned 16 bit data */
typedef unsigned long   U32BIT;     /* unsigned 32 bit data */
typedef signed char     S8BIT;      /* signed 8 bit data */
typedef signed short    S16BIT;     /* signed 16 bit data */
typedef signed long     S32BIT;     /* signed 32 bit data */

static void CRC_Calculation(unsigned char cChar, unsigned short *jCRC);

static void CRC_Calculation(unsigned char cChar, unsigned short *jCRC)
{
   unsigned char cBit;
   unsigned short  j, jCRCc;

   jCRCc = (unsigned short)cChar;

   for(cBit=0;cBit<8;jCRCc>>=1,cBit++)
   {
      j=(jCRCc^(*jCRC))&1;
      *jCRC >>=1;
      if(j)
         *jCRC ^= 0xA001;
   }
}

U16BIT calc_CRC(unsigned char data[], int sizeOfData);
U16BIT calc_CRC(unsigned char data[], int sizeOfData){
    U16BIT rxUartCrc = 0xFFFF;
    U16BIT tempCounter;
    for (tempCounter = 0; tempCounter < sizeOfData; tempCounter++)
    {
    CRC_Calculation(data[tempCounter], &rxUartCrc);
    }

    printf("crc: 0x%x", rxUartCrc);
    return rxUartCrc;
}
/*
int main(void) {

// your code goes here

U16BIT rxUartCrc = 0xFFFF;
//E9 00 15 00 01 01 FF 00 00 0C FF 00
//unsigned char data[]={0xE9,0x00,0X00, 0X0D, 0X00, 0X11, 0X03, 0X00, 0X00, 0X01, 0X12, 0X01, 0X01, 0X01, 0X12, 0X00};
//unsigned char data[]={0xE9,0x00,0X00,0X09, 0X00, 0X12, 0X03, 0X00, 0X00};
//unsigned char data[]={0xE9,0x00,0x00,0x1B,0x00,0x12,0x03,0x00,0x01,0x01,0x00,0x01,0x00,0xF0,0x03,0x0c,0xFE,0x00,0x01,0xFF,0xFE,0x00,0x00};
//unsigned char data[]={0xE9,0x00,0x00,0x1B,0x00,0x12,0x02,0x00,0xFF,0x02,0x00,0x01,0x00,0xF0,0xFF,0xFF,0xFF,0x00,0x01,0xFF,0xFE,0x00,0x00};
unsigned char data[]={0xE9,0x00,0x00,0X0D,0X00,0X13,0X01,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0X03,0XFF,0XFF,0X00};
//unsigned char *pData = &data;
int sizeofdata1;
sizeofdata1 = sizeof(data);
rxUartCrc = calc_CRC(data,sizeofdata1);

printf("crc: 0x%x", rxUartCrc);
return 0;
}
*///
