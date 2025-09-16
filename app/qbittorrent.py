from qbittorrentapi import Client

def add_download(host, port, username, password, link):
    """
    Connects to a qBittorrent client and adds a new download.
    """
    try:
        # Instantiate the client
        client = Client(
            host=host,
            port=port,
            username=username,
            password=password
        )

        # Log in to the client
        client.auth_log_in()

        # Add the download link
        result = client.torrents_add(urls=link)

        if result == "Ok.":
            print(f"Successfully sent download to qBittorrent: {link}")
            return True
        else:
            print(f"Failed to send download to qBittorrent. Response: {result}")
            return False

    except Exception as e:
        print(f"Error connecting to qBittorrent or adding download: {e}")
        return False
