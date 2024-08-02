import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector 

# Set up the MySQL connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  
    database="redbus_1"   
)
cursor = db_connection.cursor()

# Set up the webdriver
driver = webdriver.Chrome()  

# Open the target website
driver.get("https://www.redbus.in/online-booking/rtc-directory")


time.sleep(2.5)

# Extract all State Bus Route URLs from the main page
state_bus_route_elements = driver.find_elements(By.CLASS_NAME, "D113_link")
state_bus_route_links = [
    element.get_attribute("href") for element in state_bus_route_elements
]

def extract_bus_route_names_and_links():
    time.sleep(2.5)

    # Extract Bus Route Names and Links from the current page
    bus_route_elements = driver.find_elements(By.CSS_SELECTOR, ".route")
    bus_route_data = []
    for bus_route in bus_route_elements:
        bus_route_name = bus_route.text
        bus_route_href = bus_route.get_attribute("href")
        bus_route_data.append(
            {"Bus Route Name": bus_route_name, "Bus Route Link": f"{bus_route_href}"}
        )

    return bus_route_data

def extract_bus_details(bus_route_link):
    driver.get(bus_route_link)
    time.sleep(2.5)

    def scroll_to_bottom():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5) 
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def extract_from_page():
        bus_details = []
        bus_blocks = driver.find_elements(By.CSS_SELECTOR, ".clearfix.row-one")
        for block in bus_blocks:
            bus = {}
            try:
                bus["Bus Name"] = block.find_element(
                    By.CSS_SELECTOR, ".travels.lh-24.f-bold.d-color"
                ).text
            except:
                bus["Bus Name"] = "N/A"

            try:
                bus["Bus Type"] = block.find_element(
                    By.CSS_SELECTOR, ".bus-type.f-12.m-top-16.l-color.evBus"
                ).text
            except:
                bus["Bus Type"] = "N/A"

            try:
                bus["Departing Time"] = block.find_element(
                    By.CSS_SELECTOR, ".dp-time.f-19.d-color.f-bold"
                ).text
            except:
                bus["Departing Time"] = "N/A"

            try:
                bus["Duration"] = block.find_element(
                    By.CSS_SELECTOR, ".dur.l-color.lh-24"
                ).text
            except:
                bus["Duration"] = "N/A"

            try:
                bus["Reaching Time"] = block.find_element(
                    By.CSS_SELECTOR, ".bp-time.f-19.d-color.disp-Inline"
                ).text
            except:
                bus["Reaching Time"] = "N/A"

            try:
                star_rating_classes = [
                    ".lh-18.rating.rat-green span",
                    ".lh-18.rating.rat-yellow span",
                    ".lh-18.rating.rat-red span",
                ]
                star_rating = "N/A"
                for star_class in star_rating_classes:
                    try:
                        star_rating_element = block.find_element(
                            By.CSS_SELECTOR, star_class
                        )
                        star_rating = star_rating_element.text
                        break
                    except:
                        continue
                bus["Star Rating"] = star_rating
            except:
                bus["Star Rating"] = "N/A"

            # Extract price
            try:
                price_text = block.find_element(By.CSS_SELECTOR, ".fare.d-block").text
                # Remove non-numeric characters
                price_digits = ''.join(filter(str.isdigit, price_text))
                if len(price_digits) == 6:
                    bus["Price"] = float(price_digits[:3])
                elif len(price_digits) == 8:
                    bus["Price"] = float(price_digits[:4])
                else:
                    bus["Price"] = float(price_digits) if price_digits else None
            except Exception as e:
                print(f"Error extracting price: {e}")
                bus["Price"] = None

            # Extract seat availability and ignore window information
            try:
                seat_info = block.find_element(
                    By.CSS_SELECTOR, ".column-eight.w-15.fl .seat-left"
                ).text
                # Extract numeric value for seats available
                seat_digits = ''.join(filter(str.isdigit, seat_info))
                bus["Seat Availability"] = f"{seat_digits} Seats available" if seat_digits else "N/A"
            except Exception as e:
                print(f"Error extracting seat availability: {e}")
                bus["Seat Availability"] = "N/A"

            bus_details.append(bus)
        return bus_details

    all_bus_details = []

    while True:
        scroll_to_bottom()
        all_bus_details.extend(extract_from_page())

        try:
            pagination_elements = driver.find_elements(
                By.CSS_SELECTOR, ".DC_117_pageTabs"
            )
            current_page_index = None
            for i, elem in enumerate(pagination_elements):
                if "DC_117_pageActive" in elem.get_attribute("class"):
                    current_page_index = i
                    break

            if (
                current_page_index is not None
                and current_page_index < len(pagination_elements) - 1
            ):
                next_page = pagination_elements[current_page_index + 1]
                driver.execute_script(
                    "arguments[0].scrollIntoView();", next_page
                )  # Ensure the element is in view
                next_page.click()
                time.sleep(2.5)  
            else:
                break
        except Exception as e:
            print(f"Error navigating through pages: {e}")
            break

    return all_bus_details

# Collecting all data
all_data = []

# Loop through each State Bus Route Link and extract Bus Route Names and Links
for state_bus_route_link in state_bus_route_links:
    try:
        driver.get(state_bus_route_link)
        bus_route_data = extract_bus_route_names_and_links()

        # For each bus route link, extract bus details
        for bus_route in bus_route_data:
            bus_route_name = bus_route["Bus Route Name"]
            bus_route_link = bus_route["Bus Route Link"]
            bus_details = extract_bus_details(bus_route_link)

            # Store the collected data
            for bus in bus_details:
                cursor.execute(
                    """
                    INSERT INTO bus_routes 
                    (route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        bus_route_name,
                        bus_route_link,
                        bus["Bus Name"],
                        bus["Bus Type"],
                        bus["Departing Time"],
                        bus["Duration"],
                        bus["Reaching Time"],
                        (
                            float(bus["Star Rating"])
                            if bus["Star Rating"] != "N/A"
                            else None
                        ),
                        (
                            float(bus["Price"]) if bus["Price"] is not None else None
                        ),
                        (
                            int(bus["Seat Availability"].split()[0])
                            if bus["Seat Availability"] != "N/A" and bus["Seat Availability"].split()[0].isdigit()
                            else None
                        ),
                    ),
                )
                db_connection.commit()
    except Exception as e:
        print(f"Failed to load State Bus Route Link {state_bus_route_link}: {e}")

# Close the browser
driver.quit()

# Close the database connection
cursor.close()
db_connection.close()
