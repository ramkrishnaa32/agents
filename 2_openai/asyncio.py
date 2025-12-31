import asyncio

async def do_some_processing() -> str:
    print("Processing...")
    await asyncio.sleep(1)
    print("Processing completed")
    return "Done"

async def another_processing() -> str:
    print("Another processing...")
    await asyncio.sleep(1)
    print("Another processing completed")
    return "Another Done"

# Use asyncio.run() with asyncio.gather() to run multiple async functions concurrently
async def main():
    results = await asyncio.gather(do_some_processing(), another_processing())
    print(results)
    return results

# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())

