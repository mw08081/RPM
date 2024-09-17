from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags

# Define a service like so.
class MyService(Service):
    def __init__(self):
        self._some_value = None
        self.keepAdvert = True
        # Call the super constructor to set the UUID.
        super().__init__("BEEF", True)

    def get_keepAdvert(self):
        return self.keepAdvert

    # Use the characteristic decorator to define your own characteristics.
    # Set the allowed access methods using the characteristic flags.
    @characteristic("BEF0", CharFlags.READ)
    def my_readonly_characteristic(self, options):
        # Characteristics need to return bytes.
        return bytes("Hi Octa", "utf-8")

    # @characteristic("BEF1", CharFlags.WRITE).setter
    # Define a characteristic writing function like so.
    @characteristic("BEF1", CharFlags.WRITE).setter
    def my_writeonly_characteristic(self, value, options):
        # Your characteristics will need to handle bytes.
        self._some_value = value
        self.keepAdvert = False
        print('Receive Data : ', self._some_value)