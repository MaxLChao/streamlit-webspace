# Welcome to streamlit app for BMI 530 
Project for Max Chao, Ariadna Kim Silva, Haotian Xu, & Eliezer Arevera

Goals: Modeling Death in a patient cohort gathered by Janos Hajagos about length of stay.

To Run:

```
streamlit run streamlit_app.py
```

@Eliezer if you get here: Majority of the code is in that python file. More information about finetuning things can be found on the streamlit webpage.

QoLs to improve:
1. Timeline can be pretty-upped by images and other things via a media tag. I would add tags based on either the test or the category.
2. Change from tabs to maybe sidebar? Not sure which one would look nicer.
3. Clean up some inefficiencies with the data loading, super lazy with data loading. Could possibly tell how many lines to load in via `pd.read_csv` instead of editing post.
4. Should spend more time on occurences for not dead patients. What are those like?
5. Figure out a way to clean up measurements better. Can see my work in the R files attached here.
6. add occurences into clinical relationships
7. Include the basic models
8. Incorporate more of the data not used.
9. Implement some of the model visualizations

Check it out on [Streamlit Community Cloud](https://st-hello-app.streamlit.app/)

v0.1 Officially live!
[Link](https://bmi530-finalproject-eac5e44d4c623fc8.streamlit.app/)
