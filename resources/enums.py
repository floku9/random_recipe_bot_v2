from enum import Enum


class ConversationStates(str, Enum):
    START = "start"
    ASK_PREFERENCES = "ask_preferences"
    RESTRICTIONS_CHOICE = "restrictions_choice"
    EXCLUDE_PRODUCTS = "exclude_products"
    INCLUDE_PRODUCTS = "include_products"
    GIVE_RECIPE = "give_recipe"
    CONTINUE_CHOICE = "continue_choice"
    END = "end"
