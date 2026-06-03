from action_layer.gpio_controller import GPIOController


class ActionRouter:

    def __init__(self):

        self.gpio = GPIOController()

    def handle_prediction(self, prediction):

        print(f"Routing action for: {prediction}")

        self.gpio.set_prediction_led(prediction)

    def shutdown(self):

        self.gpio.cleanup()