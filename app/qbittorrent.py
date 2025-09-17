from qbittorrentapi import Client
import time

def add_download(host, port, username, password, link):
    """
    Connects to a qBittorrent client, adds a new download,
    and returns the hash of the new torrent.
    """
    try:
        client = Client(host=host, port=port, username=username, password=password)
        client.auth_log_in()

        # Get torrent hashes before adding
        hashes_before = {t.hash for t in client.torrents_info()}

        # Add the download link
        result = client.torrents_add(urls=link)
        if result != "Ok.":
            print(f"Failed to send download to qBittorrent. Response: {result}")
            return None

        # It can take a moment for the new torrent to appear in the list.
        # We'll check a few times before giving up.
        for _ in range(5):
            time.sleep(1)
            hashes_after = {t.hash for t in client.torrents_info()}
            new_hashes = hashes_after - hashes_before
            if len(new_hashes) == 1:
                new_hash = new_hashes.pop()
                print(f"Successfully added torrent with hash: {new_hash}")
                return new_hash

        print("Could not identify the newly added torrent hash after adding.")
        return None

    except Exception as e:
        print(f"Error connecting to qBittorrent or adding download: {e}")
        return None


def get_completed_torrents(host, port, username, password):
    """
    Connects to a qBittorrent client and returns a list of completed torrent hashes.
    """
    completed_hashes = []
    try:
        client = Client(
            host=host,
            port=port,
            username=username,
            password=password
        )
        client.auth_log_in()

        # Fetch all torrents and filter for completed ones
        for torrent in client.torrents_info():
            # A torrent is considered complete if its progress is 1 (100%)
            if torrent.progress == 1:
                completed_hashes.append(torrent.hash)

    except Exception as e:
        print(f"Error connecting to qBittorrent or fetching torrents: {e}")

    return completed_hashes
