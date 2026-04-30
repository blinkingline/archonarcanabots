from models.artist_model import ArtistMap
import os

def test_artist_map():
    am = ArtistMap()
    am.add_csv('skyjedi/illustrators.csv')
    
    # Check a known card from the CSV
    # I'll peek at the CSV first to find a card name
    pass

if __name__ == "__main__":
    am = ArtistMap()
    am.add_csv('skyjedi/illustrators.csv')
    # Peek at first few entries
    with open('skyjedi/illustrators.csv', 'r') as f:
        print("First few lines of CSV:")
        for i in range(5):
            print(f.readline().strip())
    
    # Test a few lookups
    test_cards = ["Daughter", "Autocannon", "Fear"]
    for card in test_cards:
        print(f"Artist for {card}: {am.get(card)}")
