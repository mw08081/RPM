import asyncio

from bluez_peripheral.advert import Advertisement
from bluez_peripheral.util import get_message_bus, Adapter
from bluez_peripheral.agent import NoIoAgent

from sHeartRateService import HeartRateService
from sMyService import MyService

# Define the releaseCallback function
def release_callback():
    print("Advertisement released")

async def register_advertisment(bus):
    # Create an advertisement with the releaseCallback
    advert = Advertisement(
        localName="RPM",
        serviceUUIDs=["180D"],  # Example UUID for Heart Rate Service
        appearance=0x0340,
        timeout=3,
    )

    adap = await Adapter.get_first(bus)
    await advert.register(bus, adap)
    print("Advertising...:", await adap.get_name() + '(' + await adap.get_address() + ')')

async def main():
    # Get the D-Bus message bus
    bus = await get_message_bus()

    service = MyService()#HeartRateService()
    await service.register(bus)

    # An agent is required to handle pairing 
    # This script needs superuser for this to work.
    agent = NoIoAgent()
    await agent.register(bus)

    # Registe Advertisment to bus
    await register_advertisment(bus)

    # Keep the script running
    while True:
        await asyncio.sleep(3)

        if service.get_keepAdvert() == True :
            await register_advertisment(bus)

    # # # 이건 구독자를 위한 반복인듯
    # # 일단추가
    # while True:
    #     val = 120
    #     service.update_heart_rate(val)

    #     val += 5
    #     # Handle dbus requests.
    #     await asyncio.sleep(5)

    await bus.wait_for_disconnect()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())