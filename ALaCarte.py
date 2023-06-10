import tkinter as tk
import requests
import json
import random
from wit import Wit
import speech_recognition as sr
from tkinter import Tk, Label, Button, messagebox, Toplevel, scrolledtext, ttk

messagebox_window = None
remaining_restaurants = []
current_restaurant_label = None

def check_restaurant_exists(name):
    with open('visited_restaurants.txt', 'r') as file:
        for line in file:
            if line.startswith('Restaurant:'):
                if name.lower() == line.strip().split(': ')[1].lower():
                    return True
    return False
def save_data():
    restaurant_name = name_entry.get()
    location = location_entry.get()

    # Validate if both fields are filled
    if not location:
        messagebox.showwarning("Error", "Please enter a location.")
        return
    if restaurant_name == "N/A":
        # Only fetch restaurant data from Yelp's API for the location
        api_key = "7G65aR12lTk2xZq9jWIE3tljqDF-JpZA6CEFhyKXa_CON_BmMTr_Hx0OVJkGb_D_3MPKQZkZQeoOP_u2NGnbPqHlRMwmxbjGN5MpWgs2R48plXW7nnWvDCQyynuCZHYx"
        restaurants = get_restaurants(api_key, location)



        if restaurants:
            # Save the fetched restaurant data to a text file
            save_restaurants_data(restaurants)
            messagebox.showinfo("Success", "Restaurant information saved.")
            # Read the contents of the restaurant_data.txt file
            with open("restaurant_data.txt", "r") as file:
                restaurant_data = file.read()

            # Show the contents in a message box
            messagebox.showinfo("Restaurant Data", restaurant_data)
        else:
            messagebox.showerror("Error", "Failed to fetch restaurant data.")
    else:
        # Validate if the restaurant name is filled
        if not restaurant_name:
            messagebox.showwarning("Error", "Please enter a restaurant name.")
            return

        if check_restaurant_exists(restaurant_name):
            messagebox.showinfo('Restaurant Already Listed', 'The restaurant is already listed.')
            return

        # Save the data to a text file
        with open("visited_restaurants.txt", "a") as file:
            file.write(f"Restaurant: {restaurant_name}\n\n")

        # Fetch restaurant data from Yelp's API
        api_key = "7G65aR12lTk2xZq9jWIE3tljqDF-JpZA6CEFhyKXa_CON_BmMTr_Hx0OVJkGb_D_3MPKQZkZQeoOP_u2NGnbPqHlRMwmxbjGN5MpWgs2R48plXW7nnWvDCQyynuCZHYx"
        restaurants = get_restaurants(api_key, location)

        if restaurants:
            # Save the fetched restaurant data to a text file
            save_restaurants_data(restaurants)
            messagebox.showinfo("Success", "Restaurant information saved.")
        else:
            messagebox.showerror("Error", "Failed to fetch restaurant data from Yelp's API.")

def get_restaurants(api_key, location):
    url = "https://api.yelp.com/v3/businesses/search"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    params = {
        "location": location,
        "categories": "restaurants"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["businesses"]
    else:
        return None

def save_restaurants_data(restaurants):
    with open("restaurant_data.txt", "w") as file:
        for restaurant in restaurants:
            name = restaurant["name"]
            location = ", ".join(restaurant["location"]["display_address"])
            phone = restaurant["phone"]
            rating = restaurant["rating"]
            review_count = restaurant["review_count"]

            file.write(f"Name: {name}\nLocation: {location}\nPhone: {phone}\nRating: {rating}\nReview Count: {review_count}\n\n")

def show_random_restaurant():
    global remaining_restaurants, current_restaurant_label

    if remaining_restaurants:
        random_restaurant = random.choice(remaining_restaurants)
        if current_restaurant_label:
            current_restaurant_label.destroy()  # Remove the previously displayed restaurant
        current_restaurant_label = Label(messagebox_window, text='\n'.join(random_restaurant))
        current_restaurant_label.pack()
        remaining_restaurants.remove(random_restaurant)  # Remove the displayed restaurant from the list
    else:
        messagebox.showinfo('No Remaining Restaurants', 'You have visited all restaurants in your area!')


def compare_files():
    global messagebox_window, remaining_restaurants, current_restaurant_label
    # Read the contents of 'restaurants.txt'
    with open('visited_restaurants.txt', 'r') as file:
        restaurant_names = [line.strip().split(': ')[1] for line in file if line.startswith('Restaurant')]

    # Read the contents of 'restaurant_data.txt' and filter out restaurants with the same names
    with open('restaurant_data.txt', 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 6):
            name = lines[i].strip().split(': ')[1]
            if name not in restaurant_names:
                remaining_restaurants.append(lines[i:i+6])

    # Display the remaining restaurants to the user
    # Create a single Toplevel window for the messagebox
    if messagebox_window:
        messagebox_window.destroy()
    messagebox_window = Toplevel()
    messagebox_window.title('Random Restaurant')
    Button(messagebox_window, text='Show me another option!', command=show_random_restaurant).pack()

    show_random_restaurant()

root = tk.Tk()
root.title("À la Carte")


location_label = tk.Label(root, text="What's Your Location? (Address, City, State Zip Code):")
location_label.pack()

location_entry = tk.Entry(root)
location_entry.pack()

name_label = tk.Label(root, text="What Restaurant Have You Visited Today? (N/A if none):")
name_label.pack()

name_entry = tk.Entry(root)
name_entry.pack()

save_button = tk.Button(root, text="Save", command=save_data)
save_button.pack()

compare_button = tk.Button(root, text='Give me a new place!', command=compare_files)
compare_button.pack()

root.mainloop()
