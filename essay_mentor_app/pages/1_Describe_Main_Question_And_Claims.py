# page 1: Describe Main Question and Claims

from typing import List

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import uuid

from essay_mentor_app.backend.aea_datamodel import (
    ArgumentativeEssayAnalysis,
    MainClaim,
    MainQuestion,
)

from essay_mentor_app.backend.components import (
    clear_associated_keys
)

st.session_state.update(st.session_state)

st.set_page_config(page_title="Main Question And Claims", page_icon="?!")
aea: ArgumentativeEssayAnalysis = st.session_state.aea


## status bar 

#st.sidebar.header("Main Question and Claims")
#progress_bar = st.sidebar.progress(0)
#status_text = st.sidebar.empty()




# main page


if not aea.essaytext_html:
    st.write(
        "You need to upload an essay first. "
        "Please go back to the previous page and do so."
    )
    st.stop()


if aea.main_questions or aea.main_claims:
    st.write("#### Your main question:")
    st.write(aea.main_questions[0].text)
    st.write("#### Your central claims:")
    for claim in aea.main_claims:
        st.write(f"* **\[{claim.label}\]**: {claim.text}")

    if st.button("Revise main question or claims"):
        clear_associated_keys(aea.objections)
        aea.objections = []
        clear_associated_keys(aea.rebuttals)
        aea.rebuttals = []
        clear_associated_keys(aea.reasons)
        aea.reasons = []
        aea.main_questions = []
        aea.main_claims = []
        st.experimental_rerun()
    if aea.reasons:
        st.caption("(Revision will delete any data that has been entered on pages hereafter.)")


    if aea.main_questions or aea.main_claims:
        st.stop()


st.info(
    "What is your essay all about?",
    icon="❔"
)
st.caption(
    "Below, enter the main question you address in the essay. "
    "Summarize the answers you discuss in the form of central claims. "
    "List only independent claims, i.e., answers you argue for without resort "
    "to each other."
)

main_question_txt = st.text_area(
    "Enter your main question here",
    height=30,
    key="main_question"
)

main_claims_txt = st.text_area(
    "Enter your central claim(s) here (separataed by empty lines)",
    height=200,
    key="central_claims"
)


# dummy siedbar info:
#i=0.2
#status_text.text("%i%% Complete" % i)
#progress_bar.progress(i)

if main_question_txt and main_claims_txt:
    n_claims = len([x for x in main_claims_txt.splitlines() if x])
    st.success(
        str(f"Main question and {n_claims} central claim(s) recognized.")
    )
elif not main_question_txt:
    st.warning("Main question is missing.")
elif not main_claims_txt:
    st.warning("Central claims are missing.")


if st.button(
    "Use this input and proceed with next step",
    disabled=not(main_question_txt and main_claims_txt)
):

    main_question = MainQuestion(
        text=main_question_txt,
    )

    counter = 0
    main_claims: List[MainClaim] = []
    for claim in main_claims_txt.splitlines():
        if claim.strip():
            counter += 1
            main_claims.append(
                MainClaim(
                    text=claim,
                    question_refs=[main_question.uid],
                    label=f"Claim{counter}",
                )
            )
            main_question.claim_refs.append(main_claims[-1].uid)

    aea.main_questions = [main_question]
    aea.main_claims = main_claims
    switch_page("Summarize Primary Arguments")



#st.write("-------")

#with st.expander("Debugging"):
#    aea: ArgumentativeEssayAnalysis = st.session_state.aea
#    if aea.main_questions:
#        st.json(aea.main_questions[0].__dict__)
#    for claim in aea.main_claims:
#        st.json(claim.__dict__)