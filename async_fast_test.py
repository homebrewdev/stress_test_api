import asyncio
import aiohttp
import time
from tqdm import tqdm
import requests
import settings


class Stress_API:
    def __init__(self, url: str):
        self.url = url

    def http_get(self, path: str, times: int):
        content = []
        for _ in tqdm(range(times), desc='Fetching data...', colour='GREEN'):
            response = requests.get(self.url + path, headers=settings.api_headers)
            content.append(response.json())
        return content

    async def async_http_get(self, path: str, times: int):
        async with aiohttp.ClientSession() as session:
            content = []
            for _ in tqdm(range(times), desc='Async fetching data...', colour='GREEN'):
                response = await session.get(url=self.url + path)
                content.append(await response.text(encoding='UTF-8'))
                print(content)
            return content


def run_case(func, path, times):
    start_timestamp = time.time()

    asyncio.run(func(path, times))

    task_time = round(time.time() - start_timestamp, 2)
    rps = round(times / task_time, 1)
    print(
        f"| Requests: {times}; Total time: {task_time} s; RPS: {rps}. |\n"
    )


if __name__ == '__main__':
    # кол-во запросов в пачке
    N = settings.stress_attempts
    # новый экземпляр стресс теста
    api = Stress_API(url=settings.URL)
    path = 'users/'
    print(f'Connect to API by url endpoint: {settings.URL + path}')
    # запуск основного процесса
    # run_case(api.async_http_get, path='fact/', times=N)
    run_case(api.async_http_get, path=path, times=N)
