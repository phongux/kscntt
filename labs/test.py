# import asyncio
# async def hold(seconds):
#     print(f'Waiting {seconds} seconds...')
#     #await asyncio.sleep(seconds)
# async def main():
#     await asyncio.gather(*[hold(1), hold(2), hold(3)])
# asyncio.run(main())

class Test:
    def abc(self):
        return 'abc'

    def bcd(self):
        return self.abc() + 'ef'

t = Test()

print(t.bcd())
