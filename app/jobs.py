from app import app, db
from app import qbittorrent
from app.models import DownloadClient, Book

def check_completed_downloads():
    """
    Checks for completed downloads and updates the status of books.
    This job is run periodically by the scheduler.
    """
    with app.app_context():
        print("Running 'check_completed_downloads' job...")
        client_config = DownloadClient.query.first()
        if not client_config:
            print("No download client configured. Skipping job.")
            return

        completed_hashes = qbittorrent.get_completed_torrents(
            host=client_config.host,
            port=client_config.port,
            username=client_config.username,
            password=client_config.password
        )

        if not completed_hashes:
            return

        # Find books that are currently downloading
        downloading_books = Book.query.filter_by(status='downloading').all()
        for book in downloading_books:
            if book.download_id in completed_hashes:
                print(f"Book '{book.title}' has completed downloading. Updating status to 'downloaded'.")
                book.status = 'downloaded'

        db.session.commit()
