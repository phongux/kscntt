import math
import concurrent.futures
import asyncio

# The definition of is_prime has been cut from this file

# Wrapping corouting which waits for return from process pool.

async def get_result(executor, n):
    loop = asyncio.get_event_loop()
    prime = await loop.run_in_executor(executor, is_prime, n)
    return n, prime

# Scheduling the run in the asyncio event loop

async def main():
    prime_candidates = [
        112272535095293,
        112582705942171,
        112272535095293,
        115280095190773,
        115797848077099,
        1099726899285419,
        17,
        4]
    # create the process pool
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Calling the asyncio coroutines returns futures.
        futures = [get_result(executor,n) for n in prime_candidates]

        # As futures are completed they are returned and the result can be obtained
