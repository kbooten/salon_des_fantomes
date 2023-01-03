from psychotropics.utterance_transformers import transformation_odd_parenthetical,transformation_expand_into_simple_words,transformation_doubt,transformation_juan
from psychotropics.character_transformers import *


prob = 0.1
step = 0.03


# prob = 0.9
# step = 0.1
input("drinks -> prob:%s, step:%s (ENTER to continue)" % (prob,step))

drinks2psycho = {
    "water":None,
    "port":None,
    "calvados":None,
    "chablis":None,
    "sherry":None,
    "amontillado":None,
    "madeira":None,
    "dry vermouth":None,
    "sweet vermouth":None,
    "scotch":None,
    "brandy":None,
    "1961 Pétrus":{
                    "function":transformation_odd_parenthetical,
                    "type":"transform_utterance",
                    "prob":prob,
                    "step":step
                    },

    "1950 Château Lafleur":{
                    "function":transformation_doubt,
                    "type":"transform_utterance",
                    "prob":prob,
                    "step":step*2
                    },

    "1962 La Tâche":{
                    "function":transformation_expand_into_simple_words,
                    "type":"transform_utterance",
                    "prob":prob*3,
                    "step":step*2
                    },

    "1996 Haut-Brion Blanc":{
                    "function":transformation_juan,
                    "type":"transform_utterance",
                    "prob":prob,
                    "step":step*3
                    },

    "Dasani":{
                    "function":word_dasani,
                    "type":"transform_character_words",
                    "prob":prob,
                    "step":step
                    },

    "1947 Cheval-Blanc":{
                    "function":word_juan,
                    "type":"transform_character_words",
                    "prob":prob,
                    "step":step
                    },

    "1945 Romanée-Conti":{
                    "function":word_new_ideology,
                    "type":"transform_character_words",
                    "prob":prob,
                    "step":step
                    },

    "1869 Chateau Lafite":{
                    "function":word_new_concept,
                    "type":"transform_character_words",
                    "prob":prob,
                    "step":step
                    },

    "1945 Mouton-Rothschild":{
                    "function":word_meta_gesture,
                    "type":"transform_character_words",
                    "prob":prob,
                    "step":step
                    },

    "1887 Chateau Margaux":{
                    "function":mode_juan,
                    "type":"transform_character_modes",
                    "prob":prob,
                    "step":step
                    },

    "1811 Chateau D'Yquem":{
                    "function":mode_self_abnegation,
                    "type":"transform_character_modes",
                    "prob":prob,
                    "step":step
                    },

    "2019 Bota Box Chardonnay":{
                    "function":disposition_sorrow,
                    "type":"transform_character_dispositions",
                    "prob":prob,
                    "step":step
                    },                

}