#include "stdio.h"
#include "project.h"
#include "cy_sar.h"

volatile int32_t adcValue = 1u;
void UartInit(void);
uint32_t currentMillis = 0;  // Variable to store current time in milliseconds

void SysTick_Handler(void){
    currentMillis++;  // Increment current time on every millisecond interrupt
}

void ADC_ISR_Callback(void){
    /* Read the ADC value */
    if (SAR_ADC_IsEndConversion(CY_SAR_RETURN_STATUS)){ // Needed to clear the interrupt
        adcValue = SAR_ADC_GetResult16(0u); // Read the value from channel 0
    }
}

int main(void){
    // Configure the UART peripheral
    Cy_SCB_UART_Init(UART_HW, &UART_config, &UART_context);
    // Enable the UART peripheral
    Cy_SCB_UART_Enable(UART_HW);
    
    Cy_SysTick_Init(CY_SYSTICK_CLOCK_SOURCE_CLK_LF, 32);  // 1ms tick interval, because CLK_Lf is 32kHz
    Cy_SysTick_EnableInterrupt();
    Cy_SysTick_SetCallback(0, SysTick_Handler);	
    
    __enable_irq();
    
    SAR_ADC_StartEx(&ADC_ISR_Callback);
    
    /* Turn on the SAR hardware. */
    SAR_ADC_IRQ_Enable();
        
    SAR_ADC_SetConvertMode(CY_SAR_START_CONVERT_CONTINUOUS);
    SAR_ADC_SetEosMask(1);
        
    /* Begin continuous conversions. */
    SAR_ADC_StartConvert();

    for (;;){
        char textToWrite[16];
        snprintf(textToWrite, sizeof(textToWrite), "%d %d\r\n", currentMillis, adcValue);
        Cy_SCB_UART_PutString(UART_HW, textToWrite);
        CyDelayUs(1000);
    }
}