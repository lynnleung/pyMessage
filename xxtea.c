// ****************************************************************************
//
//  Key Negotiate
//
// ****************************************************************************
// ****************************************************************************
//
//  xxtea.h
//
// ****************************************************************************
//#include <common.h> 
//#include <types.h> 

typedef signed char int8_t;
typedef unsigned char uint8_t;
typedef int int16_t;
typedef unsigned int uint16_t;
typedef long int32_t;
typedef unsigned long uint32_t;
typedef long long int64_t;
typedef unsigned long long uint64_t;
typedef int16_t intptr_t;
typedef uint16_t uintptr_t;
typedef unsigned char   FLAG;   
#define FALSE (0)

extern FLAG IsFinishKeyNeg;
extern uint8_t *rev;
extern uint8_t TEA_key[16];

extern uint8_t getStrLen(uint8_t *str);
extern void encryptXXTEA(uint8_t *buf, uint16_t len, uint8_t *key);
extern void decrpytXXTEA(uint8_t *buf, uint16_t len, uint8_t *key);

//#include <xxtea.h> 

FLAG IsFinishKeyNeg = FALSE;
uint8_t *rev;

#define MX (z>>5^y<<2) + (y>>3^z<<4)^(sum^y) + (k[p&3^e]^z);
#define DELTA  0x9e3779b9;
#define S_LOOPTIME 6

uint8_t TEA_key[16] = {0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x10};


/**
 ******************************************************************************
 * @funtion name    void encrypt(uint8_t *buf, uint8_t len, uint8_t *key)
 * @brief           encrypt the buf string using key, len is the lenght of buf
 ******************************************************************************
 */

void encryptXXTEA(uint8_t *buf, uint16_t len, uint8_t *key)  
{

    uint32_t *v = (uint32_t *)buf;
    uint32_t *k = (uint32_t *)key;
    uint16_t n;  
    
    if( len > 4 )
    {
        if(len%4)
        {
            n = len/4+1; 
        }
        else
        {
            n = len/4;    
        }
    }
    else
    {
        n = 2;
    }
    
    uint32_t z=v[n-1], y=v[0], sum=0, e;
    uint16_t p,q;

    q = S_LOOPTIME + 52/n;
    while (q-- > 0)
    {
        sum += DELTA;
        e = (sum >> 2) & 3;

        for(p=0; p<n-1; p++)
        {
            y = v[p+1],
            z = v[p] += MX;
        }

        y = v[0];
        z = v[n-1] += MX;
    }	
}

/**
 ******************************************************************************
 * @funtion name    void decrpyt(uint8_t *buf, uint8_t len, uint8_t *key)
 * @brief           decrypt the buf string using key, len is the lenght that is the original string. 
 ******************************************************************************
 */

void decrpytXXTEA(uint8_t *buf, uint16_t len, uint8_t *key) 
{
    uint32_t *v = (uint32_t *)buf;
    uint32_t *k = (uint32_t *)key;
    uint16_t n;
    if( len > 4 )
    {
        if(len%4)
        {
            n = len/4+1; 
        }
        else
        {
            n = len/4;    
        }
    }
    else
    {
        n = 2;
    }
    
    uint32_t z=v[n-1], y=v[0], sum=0, e;
    uint16_t p,q;

    q = S_LOOPTIME + 52/n;
    sum = q*DELTA ;

    while (sum != 0) 
    {
        e = (sum >> 2) & 3;
        for (p=n-1; p>0; p--) 
        {
            z = v[p-1];
            y = v[p] -= MX;
        }

        z = v[n-1]; 
        y = v[0] -= MX;
        sum -= DELTA; 
    }
}
