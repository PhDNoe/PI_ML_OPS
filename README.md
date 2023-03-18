![divider](https://user-images.githubusercontent.com/7065401/52071927-c1cd7100-2562-11e9-908a-dde91ba14e59.png)

# Noelia's ML_OPS Project!  👻👻


### ✅ Movie recommendation system using SVD and surprise-scikit
### ✅ API REST developed using FASTAPI


![divider](https://user-images.githubusercontent.com/7065401/52071927-c1cd7100-2562-11e9-908a-dde91ba14e59.png)

# **Part 1: Initial Exploratory Data Analysis (EDA)** 
## **Data Cleaning / Data Transformation**
![divider](https://user-images.githubusercontent.com/7065401/52071927-c1cd7100-2562-11e9-908a-dde91ba14e59.png)

<br>

### <ins>**Libraries used**</ins>

All data analysis was performed in Python, using the following libraries:
    * Pandas
    * Numpy
    * Scikit-Learn
    * Matplotlib
    * Seaborn


### <ins>**Brief data description and transformations performed on it.**</ins>


There are 4 datasets on movies and series on different streaming platforms:
- Amazon:  `./data/amazon_prime_titles.csv`
- Disney plus: `./data/disney_plus_titles.csv`
- Hulu: `./data/hulu_titles.csv`
- Netflix: `./data/netflix_title.csv`

### <ins>**Columns description**</ins>

* show_id: String s+number e.g: s125
* type: Movie/Tv Show
* title: Movie name
* director: director
* cast: cast
* country: country
* date_added: date added to platform
* release_year: release year
* rating: +13/+18/etc
* duration: duration (180 min or 3 seasons)
* listed_in: movie category (romance/drama/horror/...)
* description: movie description

---

## <ins>🔧 **Basic transformations performed**</ins>

### 🔹**Notebook: clean_platform.ipynb**<br>

1. A new `id` column was added, formed by the first letter of the platform and the `show_id`
2. Null values from `rating` column were replaced to "G" --> Mature audience
3. Dates were parsed from (Month_name day, year ) to (yyyy/mm/dd)
4. All text field were transformed to lowercase
5. In the Hulu dataset, values from the `duration` column had been mistakenly included in the `rating` column. This problem was fixed.
6. The NaNs in the `duration` column have been replaced by "0 min"
7. The `duration` column was split into two different columns (`duration_int` and `duration_type`)
8. With all these transformations, there are still several columns with missing data.<br>
> Probably many of the missing data from the `director`, `cast` and `country` columns of a dataset (for example Netflix) could be found in another dataset (e.g Amazon). **I leave it as a future task**
9. For now, all missing data will be replace with "unknown "+cast/country/...
10. A large dataframe was created, and the columns 'date_added' and 'duration' were dropped.
10. Save large dataframe to `/data/clean/all_together_clean.csv`

Note: *When work locally, I have saved each individual cleaned dataframe to a separate CSV file. But it were included in the .gitignore file*

---

### 🔹**Notebook: clean_rating.ipynb**<br>
> We need to concatenate the user reviews information, which is available in 8 .csv files
1. No missing data
2. We upload the 8 files and save the data in a big dataframe
3. We dropped `timestamp`  column
4. Column `rating` were renamed to  `score` to match up with nomenclature used in the platforms datasets
5. Save to `/data/clean/all_ratings.csv` (add to gitignore file because is too large)

---

### 🔹**Notebook: load_score_to_platform_data.ipynb**
We only merge users reviews with movie information, and save to `/data/clean/all_together_with_score`

---

![divider](https://user-images.githubusercontent.com/7065401/52071927-c1cd7100-2562-11e9-908a-dde91ba14e59.png)
# API REST
### Created using fastapi.

## 🟥 The API has not yet been deployed. Currently, it is running on localhost.


### The available routes are detailed below:

<br>

---

🟢 **GET /api**
> The API will return some info about other routes

```json
{
    "routes": {
        "/api/max_duration": "Movie with longer duration with optional filters of year, platform and duration_type",
        "/api/score_count": "Number of films by platform with a score greater than XX in a given year",
        "/api/count_platform": "Number of movies per platform. The platform must be specified.",
        "/api/actor": "Actor who appears the most times according to platform and year. "
    }
}

```

---

🟢 **GET /api/max_duration**
> If called without query parameters, the API will return the movie with the longest duration across all platforms, years, and duration types (seasons or minutes)

```json
{
    "movie": "soothing surf at del norte for sleep black screen"
}

```

🟢 **GET /api/max_duration?year=2019**
> The API will return the movie with the longest duration across all platforms and duration types (seasons or minutes) for the 2019 year
```json
{
    "movie": "box fan medium  8 hours for sleep"
}

```


🟢 **GET /api/max_duration?platform=netflix**
> The API will return the movie with the longest duration on Netflix across all years and duration types.
```json
{
    "movie": "box fan medium  8 hours for sleep"
}

```

🟢 **GET /api/max_duration?year=2020&platform=Netflix&duration_type=seasons**
> The API will return the Netflix movie with the longest duration measured in seasons for the year 2019
```json
{
    "movie": "grey's anatomy"
}
```

🟡 **If any of the above queries do not match any results, the API will return:**
```json
{
    "message": "No results"
}
```

---

🟢 **GET /api/score_count?platform=Netflix&scored=3.6&year=2020**
> The API will return the number of films by platform=Netflix  with a score greater than XX=3.6 in a given year (2020)
```json
{
    "number_of_films": 71
}
```

---

🟢 **GET api/count_platform?platform=amazon**
> The API will return Number of movies per platform (Amazon)
```json
{
    "number_of_films": 9668
}
```

🟡 **If the platform is not Netflix, Amazon, Hulu or Disney (or any variations of their names in lowercase), the API will return**

```json
{
    "detail": [
        {
            "loc": [
                "query",
                "platform"
            ],
            "msg": "value is not a valid enumeration member; permitted: 'disney', 'netflix', 'amazon', 'hulu', 'Disney', 'Netflix', 'Amazon', 'Hulu'",
            "type": "type_error.enum",
            "ctx": {
                "enum_values": [
                    "disney",
                    "netflix",
                    "amazon",
                    "hulu",
                    "Disney",
                    "Netflix",
                    "Amazon",
                    "Hulu"
                ]
            }
        }
    ]
}
```

---
🟢 **GET /api/actor?platform=Netflix&year=2019**
> The API will return the actor who appears the most times according to platform and year specified.
```json
{
    "actor": "vincent tong"
}
```

🟡 **If the query do not match any results, the API will return:**
```json
{
    "message": "No results"
}
```

---