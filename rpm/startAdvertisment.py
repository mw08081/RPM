import asyncio

from bluez_peripheral.advert import Advertisement
from bluez_peripheral.util import get_message_bus, Adapter
from bluez_peripheral.agent import NoIoAgent
from testService import HeartRateService



# Define the releaseCallback function
def release_callback():
    print("Advertisement released")

async def main():
    # Get the D-Bus message bus
    bus = await get_message_bus()

    # 일단추가
    service = HeartRateService()
    await service.register(bus)


     # An agent is required to handle pairing 
    agent = NoIoAgent()
    # This script needs superuser for this to work.
    await agent.register(bus)

    # Create an advertisement with the releaseCallback
    advert = Advertisement(
        localName="RPM",
        serviceUUIDs=["180D"],  # Example UUID for Heart Rate Service
        appearance=0x0340,
        timeout=0,
        releaseCallback=release_callback  # Ensure this matches the constructor
    )

    adap = await Adapter.get_first(bus)
    await advert.register(bus, adap)
    print("Advertising...:", await adap.get_name() + '(' + await adap.get_address() + ')')

    # # Keep the script running
    # while True:
    #     await asyncio.sleep(1)


    # 일단추가
    while True:
        val = 120
        service.update_heart_rate(val)

        val += 5
        # Handle dbus requests.
        await asyncio.sleep(5)

    await bus.wait_for_disconnect()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())