import csv
from collections import defaultdict
import os
import json
import requests
from json import JSONDecodeError


def download_json(url, filename):
    try:
        if os.path.exists(filename):
            return

        # Download the file from the URL
        try:
            response = requests.get(url)
            data = response.text

            # Save the data to a local file
            with open(filename, "w", encoding="utf-8") as file:
                # Write the data to the json file
                file.write(data)
            return

        except requests.exceptions.RequestException as e:
            print(f"Error downloading JSON file: {e}")
            return
    except JSONDecodeError as e:
        return


def process_recipes(recipes_data):
    chilies_recipes = {}
    difficulty_levels = defaultdict(list)
    difficulty = ""

    for recipe in recipes_data:
        # Check if the recipe contains chilies
        ingredients = recipe.get("ingredients", [])
        if "Chilies".casefold() in ingredients.casefold() or "Chiles".casefold() in ingredients.casefold() or "Chili".casefold() in ingredients.casefold():
            chilies_recipes[recipe.get("name")] = recipe

            # Calculate total time and difficulty
            prep_time = recipe.get("prepTime", 0)
            cook_time = recipe.get("cookTime", 0)

            # NOTE: took assumption for Unknown. If both prepTime and cookTime are empty, then difficulty is Unknown
            if prep_time == "" and cook_time == "":
                continue

            prep_time = prep_time.replace("PT", "")
            cook_time = cook_time.replace("PT", "")

            # check if the time is in minutes or hours
            cook_time, prep_time = convert_time(cook_time, prep_time)

            total_time = prep_time + cook_time

            if total_time > 60:
                difficulty = "Hard"
            elif 30 <= total_time <= 60:
                difficulty = "Medium"
            elif total_time < 30:
                difficulty = "Easy"

            # Add difficulty to the recipe
            recipe["difficulty"] = difficulty
            difficulty_levels[difficulty].append(total_time)

    return chilies_recipes, difficulty_levels


def convert_time(cook_time, prep_time):
    # Convert time to minutes 1h20M
    if "H" in cook_time:
        if "M" in cook_time:  # both hours and minutes
            #1h20M
            hours = int(cook_time.split("H")[0])
            minutes = int(cook_time.split("H")[1].replace("M", ""))
            cook_time = (hours * 60) + minutes

        else:  # only hours
            cook_time = int(cook_time.replace("H", "")) * 60
    elif "M" in cook_time:  # only minutes
        cook_time = int(cook_time.replace("M", ""))
    else:
        cook_time = 0

    if "H" in prep_time:
        if "M" in prep_time:
            hours = int(prep_time.split("H")[0])
            minutes = int(prep_time.split("H")[1].replace("M", ""))
            prep_time = (hours * 60) + minutes
        else:
            prep_time = int(prep_time.replace("H", "")) * 60
    elif "M" in prep_time:
        prep_time = int(prep_time.replace("M", ""))
    else:
        prep_time = 0

    return cook_time, prep_time


# Function to write data to CSV
def write_to_csv(data, filename, delimiter="|"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        writer.writerow(["name", "ingredients", "url", "image", "recipeYield", "datePublished", "prepTime", "cookTime",
                         "difficulty"])

        for recipe in data.values():
            writer.writerow([
                recipe.get("name", ""),
                recipe.get("ingredients", ""),
                recipe.get("url", ""),
                recipe.get("image", ""),
                recipe.get("recipeYield", ""),
                recipe.get("datePublished", ""),
                recipe.get("prepTime", ""),
                recipe.get("cookTime", ""),
                recipe.get("difficulty", "")
            ])


# Function to calculate average total time and write to Results.csv
def write_results(difficulty_levels, filename):
    # (Hard|AverageTotalTime|45700)  # TODO: validate if third parameter is the total time(Assumption taken)
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="|")
        #writer.writerow(["Difficulty", "AverageTotalTime", "TotalTime"])

        for difficulty, times in difficulty_levels.items():
            average_time = sum(times) / len(times)
            total_time = sum(times)
            writer.writerow([difficulty, average_time, total_time])


# Main function
def main():
    # Download JSON file
    json_url = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"
    file_name = "bi_recipes.json"
    download_json(json_url, file_name)

    # read local file
    json_data = []
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            # Strip leading/trailing whitespace and newlines
            line = line.strip()
            if line:
                # Parse the line as JSON and append to the list
                json_data.append(json.loads(line))

    # Process recipes
    chilies_recipes, difficulty_levels = process_recipes(json_data)

    # Write the recipes to a CSV file
    write_to_csv(chilies_recipes, "recipes-etl/Chilies.csv")
    # Write the results to a CSV file
    write_results(difficulty_levels, "recipes-etl/Results.csv")

    print(f"Processed {len(chilies_recipes)} recipes with chilies")


if __name__ == "__main__":
    main()
