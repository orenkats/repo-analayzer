import aiohttp


class GitHubClient:
    """
    A client to manage the connection with GitHub's API.
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str):
        """
        Initialize the GitHubClient with a personal access token.
        """
        self.headers = {"Authorization": f"token {token}"} if token else {}
        self.session = aiohttp.ClientSession(headers=self.headers)

    async def get(self, url: str):
        """
        Perform a GET request to the given URL.
        """
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.json()

    async def fetch_raw(self, url: str):
        """
        Perform a GET request to fetch raw file content.
        """
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    async def close(self):
        """
        Close the aiohttp.ClientSession when done.
        """
        await self.session.close()
