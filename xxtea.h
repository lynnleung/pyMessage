// ****************************************************************************
//
//  xxtea.h
//
// ****************************************************************************
//#include <common.h> 
#include <types.h> 

extern FLAG IsFinishKeyNeg;
extern uint8_t *rev;
extern uint8_t TEA_key[16];

extern uint8_t getStrLen(uint8_t *str);
extern void encryptXXTEA(uint8_t *buf, uint16_t len, uint8_t *key);
extern void decrpytXXTEA(uint8_t *buf, uint16_t len, uint8_t *key);

