import streamlit as st
from recommend_recipe import *
from search_recipe_page import *

def recommend_similar_recipe_page(recipe_number):
    answer = recommend_recipe(recipe_number)
    display_recipes_with_checkboxes(answer)