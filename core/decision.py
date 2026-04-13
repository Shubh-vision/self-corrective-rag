# ================== DECISION FUNCTIONS =========================================================================


def eval_decision(state):
    e = state['evaluation']

    if e.relevant == "no":
        return "rewrite"   # ❌ stop loop
    
    elif e.grounded == "no":
        return "human"   # ❌ stop loop
    
    elif e.answer_question == "no":
        return "human"   # ❌ stop loop
    
    else:
        return "human"
    
# def human_decision(state):
#     if state['feedback'] == "accept":
#         return "summarize"
#     elif state['feedback'] == "retry":
#         return "rewrite"
#     else:
#         return "summarize"
