
import deeplake
scraped_data = deeplake.open_read_only(f"al://activeloop/restaurant_reviews_complete")

print(f"Scraped {len(scraped_data)} reviews")


