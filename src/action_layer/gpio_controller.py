try:
    import lgpio

    GPIO_AVAILABLE = True

except ImportError:

    GPIO_AVAILABLE = False

    print("lgpio not available (development mode)")


class GPIOController:

    def __init__(self):

        self.enabled = GPIO_AVAILABLE

        # GPIO pin mapping
        self.LED_PINS = {
            "cats": 16,
            "dogs": 20,
            "others": 21
        }

        if self.enabled:

            self.h = lgpio.gpiochip_open(0)

            for pin in self.LED_PINS.values():

                lgpio.gpio_claim_output(
                    self.h,
                    pin
                )

                lgpio.gpio_write(
                    self.h,
                    pin,
                    0
                )

            print("GPIO initialized")

        else:

            print("GPIO disabled")

    def set_prediction_led(self, label):

        if not self.enabled:

            print(f"[SIM GPIO] {label}")

            return

        for key, pin in self.LED_PINS.items():

            value = 1 if key == label else 0

            lgpio.gpio_write(
                self.h,
                pin,
                value
            )

    def cleanup(self):

        if self.enabled:

            lgpio.gpiochip_close(self.h)

            print("GPIO cleaned up")