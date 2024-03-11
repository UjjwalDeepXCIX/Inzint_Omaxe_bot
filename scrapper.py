import requests
from bs4 import BeautifulSoup

# List of URLs to scrape
urls =[
    "https://www.omaxe.com/blog/omaxe-world-street-bags-estatesmen-awards-for-best-retail-project/",
    "https://www.omaxe.com/blog/where-should-you-invest-in-lucknow/",
    "https://www.omaxe.com/blog/chandigarh-a-perfect-penthouse-destination/",
    "https://www.omaxe.com/blog/commercial-space-in-capital-search-ends-here/",
    "https://www.omaxe.com/blog/modular-steel-structure-at-omaxe-chowk-a-game-changer-in-real-estate/",
    "https://www.omaxe.com/blog/choosing-among-the-best-apartment-in-lucknow/",
    "https://www.omaxe.com/blog/best-time-to-buy-your-dream-home-in-lucknow/",
    "https://www.omaxe.com/blog/real-estate-sector-trends-in-2021/",
    "https://www.omaxe.com/blog/omaxe-chowk-bestowed-with-multiple-awards/",
    "https://www.omaxe.com/blog/is-real-estate-in-india-a-profitable-investment/",
    "https://www.omaxe.com/blog/5-things-you-must-consider-before-buying-a-commercial-space/",
    "https://www.omaxe.com/blog/top-10-reasons-to-invest-in-new-chandigarh-property-market/",
    "https://www.omaxe.com/blog/things-to-consider-while-looking-for-independent-houses-for-sale-in-allahabad/",
    "https://www.omaxe.com/blog/right-time-to-buy-the-best-4-bhk-apartments-in-lucknow/",
    "https://www.omaxe.com/blog/this-diwali-invest-in-your-ream-home-by-omaxe-indore/",
    "https://www.omaxe.com/blog/3-bhk-flats-for-sale-in-ludhiana/",
    "https://www.omaxe.com/blog/omaxe-sets-target-to-become-debt-free-by-second-quarter-of-fy23/",
    "https://www.omaxe.com/blog/omaxe-faridabad-make-your-business-visible/",
    "https://www.omaxe.com/blog/omaxe-delhi-business-with-capital/",
    "https://www.omaxe.com/blog/the-face-of-real-estate-in-india/",
    "https://www.omaxe.com/blog/nri-the-new-leg-of-investor/",
    "https://www.omaxe.com/blog/5-tips-to-prepare-yourself-before-starting-a-career-in-real-estate/",
    "https://www.omaxe.com/blog/eyeing-2-bhk-flats-in-lucknow/",
    "https://www.omaxe.com/blog/construction-of-parking-in-chandni-chowk-gets-a-fillip/",
    "https://www.omaxe.com/blog/property-with-assured-returns-in-india/",
    "https://www.omaxe.com/blog/penthouse-for-sale-in-chandigarh/",
    "https://www.omaxe.com/blog/property-with-guaranteed-returns-in-india/",
    "https://www.omaxe.com/blog/is-real-estate-the-right-investment-option-versus-others/",
    "https://www.omaxe.com/blog/how-to-find-your-dream-property-online-during-lockdown/",
    "https://www.omaxe.com/blog/omaxe-city-an-oasis-of-modern-living-in-indore/",
    "https://www.omaxe.com/blog/commercial-shops-for-sale-in-chandni-chowk-delhi/",
    "https://www.omaxe.com/blog/reasons-to-invest-in-growing-real-estate-of-delhi/",
    "https://www.omaxe.com/blog/upcoming-luxury-mall-in-delhi-ncr-omaxe-chowk-mall-in-chandni-chowk/",
    "https://www.omaxe.com/blog/top-five-localities-to-invest-in-delhi-ncr/",
    "https://www.omaxe.com/blog/five-reasons-to-book-commercial-space-in-omaxe-chowk/",
    "https://www.omaxe.com/blog/rediscovering-chandni-chowk-beyond-the-space/",
    "https://www.omaxe.com/blog/chandni-chowk-delhi-a-walkthrough-on-streets/",
    "https://www.omaxe.com/blog/omaxe-chowk-retail-shops-parking-and-food-court/",
    "https://www.omaxe.com/blog/delhi-chandni-chowk-history-and-market-of-delhi/",
    "https://www.omaxe.com/blog/omaxe-chowk-parking-solution-in-chandni-chowk/",
    "https://www.omaxe.com/blog/chandni-chowk-indias-heritage-and-asias-biggest-shopping-hub/",
    "https://www.omaxe.com/blog/chandni-chowk-explore-delhis-biggest-shopping-hub/",
    "https://www.omaxe.com/blog/chandni-chowk-and-lal-qila-top-the-list-of-must-visit-places-in-delhi/",
    "https://www.omaxe.com/blog/now-get-the-ganga-views-from-your-home/",
    "https://www.omaxe.com/blog/take-a-trip-to-nearby-places-of-ludhiana/",
    "https://www.omaxe.com/blog/omaxe-connaught-place-ocp-is-a-mall-with-a-theme-park/",
    "https://www.omaxe.com/blog/dear-genius-welcome-to-the-lake/",
    "https://www.omaxe.com/blog/buy-a-property-in-new-chandigarh-and-experience-a-modern-life/",
    "https://www.omaxe.com/blog/an-ideal-home-with-a-perfect-view-of-the-holy-ganga/",
    "https://www.omaxe.com/blog/most-interesting-things-to-do-in-lucknow/",
    "https://www.omaxe.com/blog/most-trusted-brand-in-real-estate-omaxe/",
    "https://www.omaxe.com/blog/why-allahabad-is-the-place-to-invest-in-property/",
    "https://www.omaxe.com/blog/home-in-new-lucknow/",
    "https://www.omaxe.com/blog/sangam-sadhus-and-traditions-kumbh-mela-in-prayagraj/",
    "https://www.omaxe.com/blog/real-estate-in-new-chandigarh/",
    "https://www.omaxe.com/blog/ludhiana-the-city-defining-punjabs-urbanism/",
    "https://www.omaxe.com/blog/ganga-yamuna-ka-sangam/",
    "https://www.omaxe.com/blog/amazing-places-you-must-visit-in-prayagraj-during-kumbh/",
    "https://www.omaxe.com/blog/life-at-omaxe-homes-new-chandigarh/",
    "https://www.omaxe.com/blog/live-lavishly-with-the-lavish-penthouse-in-ludhiana-city/",
    "https://www.omaxe.com/blog/the-city-where-the-ganga-jamuna-and-saraswati-meets/",
    "https://www.omaxe.com/blog/planning-to-buy-a-3-bhk-flat-in-new-lucknow/",
    "https://www.omaxe.com/blog/beautiful-penthouse-in-ludhiana/",
    "https://www.omaxe.com/blog/luxurious-penthouse-in-ludhiana-the-royal-meridian/",
    "https://www.omaxe.com/blog/what-are-the-things-to-look-for-before-buying-a-3-bhk-flat/",
    "https://www.omaxe.com/blog/omaxe-offers-you-dream-home-in-new-chandigarh/",
    "https://www.omaxe.com/blog/omaxe-metro-city-in-new-lucknow/",
    "https://www.omaxe.com/blog/here-why-owning-property-in-new-chandigarh-is-a-great-idea/",
    "https://www.omaxe.com/blog/places-you-must-visit-in-lucknow/",
    "https://www.omaxe.com/blog/the-new-version-of-lucknow-is-a-new-version-of-life/",
    "https://www.omaxe.com/blog/using-lighting-to-enhance-your-space/",
    "https://www.omaxe.com/blog/the-difference-between-lofts-and-studios/",
    "https://www.omaxe.com/blog/kitchen-ideas-for-modern-families/",
    "https://www.omaxe.com/blog/office-space-interior-optimization/",
    "https://www.omaxe.com/blog/innovations-that-will-blow-your-mind/",
    "https://www.omaxe.com/blog/amazing-design-for-cozy-rooms/",
    "https://www.omaxe.com/blog/big-city-life-trending-colors/",
    "https://www.omaxe.com/blog/building-your-house-from-scratch/",
    "https://www.omaxe.com/blog/tips-for-diy-decoration-stuff/",
    "https://www.omaxe.com/blog/modern-bathroom-designs/",
    "https://www.omaxe.com/blog/professional-designers-in-your-area/",
    "https://www.omaxe.com/blog/are-you-sure-about-the-color/",
    "https://www.omaxe.com/blog/smaller-cities-smarter-choice/",
    "https://www.omaxe.com/blog/metro-city-run-lucknow/",
    "https://www.omaxe.com/blog/diwali-padadigm-shift-indian-real-estate/",
    "https://www.omaxe.com/blog/complete-your-festivities-with-smart-investments/",
    "https://www.omaxe.com/blog/ganesh-chaturthi-celebration-omaxe/",
    "https://www.omaxe.com/blog/falling-rupee-can-be-a-boon-for-nri-investments/",
    "https://www.omaxe.com/blog/invest-in-real-estate-with-low-cash/",
    "https://www.omaxe.com/blog/rising-power-of-real-estate-in-india/",
    "https://www.omaxe.com/blog/vastu-tips-for-office/",
    "https://www.omaxe.com/blog/the-emergence-of-krishna-castle/",
    "https://www.omaxe.com/blog/five-things-consider-buying-retirement-home/",
    "https://www.omaxe.com/blog/7-tips-for-designing-office-decor/",
    "https://www.omaxe.com/blog/why-buying-property-is-best-form-of-investment/",
    "https://www.omaxe.com/blog/rera-purchasing-property-made-easy/",
    "https://www.omaxe.com/blog/penalties-under-rera-across-different-states-india/",
    "https://www.omaxe.com/blog/omaxe-ideology/",
    "https://www.omaxe.com/blog/real-estate-a-real-changer-in-india/",
    "https://www.omaxe.com/blog/world-street-retailers-meet/",
    "https://www.omaxe.com/blog/homes-a-lifetime-investment/",
    "https://www.omaxe.com/blog/gst-a-needful-reform-for-real-estate/",
    "https://www.omaxe.com/blog/how-gst-rera-simplified-home-buying/",
    "https://www.omaxe.com/blog/5-magnificent-monuments-of-delhi/",
    "https://www.omaxe.com/blog/high-street-apartments/",
    "https://www.omaxe.com/blog/executive-homez-a-home-amidst-the-land-of-colours-and-culture/",
    "https://www.omaxe.com/blog/the-perfect-guide-to-relocating-your-house/",
    "https://www.omaxe.com/blog/5-common-myths-on-home-loans/",
    "https://www.omaxe.com/blog/will-rera-empower-real-estate-builders/",
    "https://www.omaxe.com/blog/faridabad-city-to-settle-in-ncr/",
    "https://www.omaxe.com/blog/different-types-of-mortgages/",
    "https://www.omaxe.com/blog/vastu-tips-for-home/",
    "https://www.omaxe.com/blog/must-know-tips-for-first-time-home-buyers-india-2017/",
    "https://www.omaxe.com/projects/search?project_city_id[0]=12&project_category[0]=1&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_city_id[0]=12&project_category[0]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_stamp_id[0]=2&project_stamp_id[1]=5&project_stamp_id[2]=11&project_stamp_id[3]=13&project_stamp_id[4]=14&project_stamp_id[5]=18&project_stamp_id[6]=19&project_stamp_id[7]=21&project_city_id[0]=12&project_category[0]=1&project_category[1]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_stamp_id[0]=3&project_stamp_id[1]=4&project_stamp_id[2]=7&project_stamp_id[3]=16&project_stamp_id[4]=20&project_stamp_id[5]=22&project_city_id[0]=12&project_category[0]=1&project_category[1]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?exclusive=1&project_city_id[0]=12&project_category[0]=1&project_category[1]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_city_id[0]=23&project_category[0]=1&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_city_id[0]=23&project_category[0]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_stamp_id[0]=2&project_stamp_id[1]=5&project_stamp_id[2]=11&project_stamp_id[3]=13&project_stamp_id[4]=14&project_stamp_id[5]=18&project_stamp_id[6]=19&project_stamp_id[7]=21&project_city_id[0]=23&project_category[0]=1&project_category[1]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_stamp_id[0]=3&project_stamp_id[1]=4&project_stamp_id[2]=7&project_stamp_id[3]=16&project_stamp_id[4]=20&project_stamp_id[5]=22&project_city_id[0]=23&project_category[0]=1&project_category[1]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?exclusive=1&project_city_id[0]=23&project_category[0]=1&project_category[1]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_city_id[0]=22&project_category[0]=1&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_city_id[0]=22&project_category[0]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_stamp_id[0]=2&project_stamp_id[1]=5&project_stamp_id[2]=11&project_stamp_id[3]=13&project_stamp_id[4]=14&project_stamp_id[5]=18&project_stamp_id[6]=19&project_stamp_id[7]=21&project_city_id[0]=22&project_category[0]=1&project_category[1]=2&all_cities=&sort_by=relevance",
    "https://www.omaxe.com/projects/search?project_stamp_id[0]=3&project_stamp_id[1]=4&project_stamp_id[2]=7&project_stamp_id[3]=16&project_stamp_id[4]=20&project_stamp_id[5]=22&project_city_id[0]=22&project_category[0]=1&project_category[1]=2&all_cities=&sort_by=relevance"
]


# Define the file name to save the text data
file_name = "omaxe_blog_data.txt"

# Open the file in write mode
with open(file_name, "w", encoding="utf-8") as file:
    # Iterate through each URL
    for url in urls:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract visible text content from the HTML
        visible_texts = soup.stripped_strings

        # Write the URL as a header in the file
        file.write(f"URL: {url}\n\n")

        # Write the extracted text data to the file
        for text in visible_texts:
            file.write(text + "\n")

        # Add a separator between different URLs
        file.write("\n" + "-"*50 + "\n\n")

print(f"Text data saved successfully to '{file_name}'.")
