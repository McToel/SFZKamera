#include "mbed.h"
#include "platform/mbed_thread.h"

Thread blink_led;
Thread read_sensors;

AnalogIn aa0(A0);
AnalogIn aa1(A1);
AnalogIn aa2(A2);
AnalogIn aa4(A4);
AnalogIn aa5(A5);

DigitalIn button(USER_BUTTON); //Onboard Button
DigitalOut led(LED1); //Onboard LED

class LongTimeTimer
{
    private:
        Timer clock;
        int runs = 0;
        const double max_time = 4294.9673;
        double last_time;
    public:
        LongTimeTimer()
        {
            clock.start();
        }
        unsigned int get_time()
        {
            double c = clock.read();
            if (c < last_time)
                runs++;
            last_time = c;
            return (unsigned int)(c + runs * max_time);
        }
};


void blink_thread() {
    while(true) {
        led = 1;
        ThisThread::sleep_for(100);
        led = 0;
        ThisThread::sleep_for(500);
    }
}

int main()
{ 
    blink_led.start(blink_thread);
    
    LongTimeTimer timer;
    while(true) {
        unsigned int time = timer.get_time();
        printf("%u", time);
        

        printf(",%u", aa0.read_u16());
        ThisThread::sleep_for(1);
        printf(",%u", aa1.read_u16());
        ThisThread::sleep_for(1);
        printf(",%u", aa2.read_u16());
        ThisThread::sleep_for(1);
        printf(",%u", aa4.read_u16());
        ThisThread::sleep_for(1);
        printf(",%u", aa5.read_u16());
        
        printf("\n");
        ThisThread::sleep_for(1000);
    }
    
}
