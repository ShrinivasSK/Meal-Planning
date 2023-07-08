## Dataset for Meal Planning

### File Structure

- Culinary DB: Data from Culinary DB dataset
- Models: Word2VEc models trained for learning combination value between dishes in the dataset
- Processed: All the processed data of the dataset
    - Graphs: Co-occurence graph of the dishes built from the Meal Plans
    - dishes.csv: Data of all the recipes (ID, Title, Category (appetizer, main-dish, desert), Cuisine, Calories, Fats, Proteins, Carbohydrates, is it a Breakfast, Lunch, Snacks or Dinner dish, Typical serving size, Tags (some attributes for the recipes))
    - ingredients.csv: Data of different ingredients (ID, Name )
    - rec_ing.csv: Ingredient list for the recipes (list of recipe ID and ingredient ID)
    - rec_vecs.npy: Recipe vectors saved as a weighted combination of ingredient vectors

