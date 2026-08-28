import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Virtual Oracle",
    page_icon="🔮",
    layout="wide"
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.hero {
    padding: 28px;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827, #374151);
    color: white;
    margin-bottom: 20px;
}

.card {
    padding: 18px;
    border: 1px solid #dddddd;
    border-radius: 16px;
    margin-bottom: 12px;
}

.big-pick {
    font-size: 1.5rem;
    font-weight: 700;
}

.small {
    color: #777777;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Prediction Engine
# -----------------------------
def predict(
    h2h_home=0.50,
    home_form=0.50,
    away_form=0.50,
    over_rate=0.50,
    draw_rate=0.25
):

    home_strength = (
        0.42 * h2h_home
        + 0.25 * home_form
        + 0.13 * (1 - away_form)
        + 0.10 * over_rate
        + 0.10 * (1 - draw_rate)
    )

    away_strength = (
        0.42 * (1 - h2h_home)
        + 0.25 * away_form
        + 0.13 * (1 - home_form)
        + 0.10 * over_rate
        + 0.10 * (1 - draw_rate)
    )

    draw_strength = (
        0.55 * draw_rate
        + 0.45 * (1 - abs(home_strength - away_strength))
    )

    home_strength = max(0.001, home_strength)
    draw_strength = max(0.001, draw_strength)
    away_strength = max(0.001, away_strength)

    total = (
        home_strength
        + draw_strength
        + away_strength
    )

    home_probability = home_strength / total
    draw_probability = draw_strength / total
    away_probability = away_strength / total

    probabilities = {
        "HOME": home_probability,
        "DRAW": draw_probability,
        "AWAY": away_probability
    }

    prediction = max(
        probabilities,
        key=probabilities.get
    )

    confidence = probabilities[prediction]

    # Experimental score estimate
    if prediction == "HOME":

        if draw_probability >= 0.22:
            score = "2-1"
        else:
            score = "2-0"

    elif prediction == "AWAY":

        if draw_probability >= 0.22:
            score = "1-2"
        else:
            score = "0-2"

    else:
        score = "1-1"

    return (
        probabilities,
        prediction,
        confidence,
        score
    )


# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">

<h1>🔮 Virtual Oracle</h1>

<p>
Personal Virtual Football Prediction &
Backtesting Laboratory
</p>

</div>
""", unsafe_allow_html=True)


st.info(
    "This is a statistical prediction prototype. "
    "It does not guarantee betting results."
)


# -----------------------------
# Tabs
# -----------------------------
tabs = st.tabs([
    "🔮 Predictor",
    "📊 Backtest",
    "📷 Screenshot",
    "📚 Data",
    "ℹ️ About"
])


# =====================================================
# PREDICTOR
# =====================================================

with tabs[0]:

    st.subheader("Single Match Prediction")

    col1, col2 = st.columns(2)

    with col1:
        home_team = st.text_input(
            "Home Team",
            "Team A"
        )

    with col2:
        away_team = st.text_input(
            "Away Team",
            "Team B"
        )


    st.markdown("### Historical Inputs")

    col1, col2, col3 = st.columns(3)

    with col1:

        h2h_home = st.slider(
            "H2H Home Share",
            0.0,
            1.0,
            0.50,
            0.01
        )

    with col2:

        home_form = st.slider(
            "Home Form",
            0.0,
            1.0,
            0.50,
            0.01
        )

    with col3:

        away_form = st.slider(
            "Away Form",
            0.0,
            1.0,
            0.50,
            0.01
        )


    col1, col2 = st.columns(2)

    with col1:

        over_rate = st.slider(
            "Over Rate",
            0.0,
            1.0,
            0.50,
            0.01
        )

    with col2:

        draw_rate = st.slider(
            "Draw Rate",
            0.0,
            1.0,
            0.25,
            0.01
        )


    if st.button(
        "🔮 GENERATE PREDICTION",
        type="primary",
        use_container_width=True
    ):

        probabilities, prediction, confidence, score = predict(
            h2h_home,
            home_form,
            away_form,
            over_rate,
            draw_rate
        )

        st.subheader(
            f"{home_team} vs {away_team}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "HOME",
                f"{probabilities['HOME'] * 100:.1f}%"
            )

        with col2:
            st.metric(
                "DRAW",
                f"{probabilities['DRAW'] * 100:.1f}%"
            )

        with col3:
            st.metric(
                "AWAY",
                f"{probabilities['AWAY'] * 100:.1f}%"
            )


        st.success(
            f"Prediction: {prediction}"
        )

        st.metric(
            "Confidence",
            f"{confidence * 100:.1f}%"
        )

        st.metric(
            "Experimental Correct Score",
            score
        )

        st.caption(
            "Confidence represents the model's calculated probability, "
            "not a guaranteed winning probability."
        )


# =====================================================
# BACKTEST
# =====================================================

with tabs[1]:

    st.subheader(
        "📊 Backtest Prediction Model"
    )

    st.write(
        "Upload historical match data to see how "
        "the prediction model performs."
    )


    template = pd.DataFrame([
        {
            "home": "Team A",
            "away": "Team B",
            "h2h_home": 0.55,
            "home_form": 0.60,
            "away_form": 0.45,
            "over_rate": 0.55,
            "draw_rate": 0.25,
            "actual": "HOME"
        }
    ])


    st.download_button(
        "⬇️ Download CSV Template",
        template.to_csv(index=False),
        "virtual_oracle_template.csv",
        "text/csv"
    )


    uploaded_file = st.file_uploader(
        "Upload Historical CSV",
        type=["csv"]
    )


    if uploaded_file:

        df = pd.read_csv(
            uploaded_file
        )


        required_columns = [
            "home",
            "away",
            "h2h_home",
            "home_form",
            "away_form",
            "over_rate",
            "draw_rate",
            "actual"
        ]


        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]


        if missing_columns:

            st.error(
                "Missing columns: "
                + ", ".join(missing_columns)
            )

        else:

            results = []


            for _, row in df.iterrows():

                probabilities, prediction, confidence, score = predict(
                    row["h2h_home"],
                    row["home_form"],
                    row["away_form"],
                    row["over_rate"],
                    row["draw_rate"]
                )


                actual = str(
                    row["actual"]
                ).upper().strip()


                results.append({

                    "Home":
                        row["home"],

                    "Away":
                        row["away"],

                    "Prediction":
                        prediction,

                    "Confidence %":
                        round(
                            confidence * 100,
                            1
                        ),

                    "Correct Score":
                        score,

                    "Actual":
                        actual,

                    "Correct":
                        prediction == actual
                })


            results_df = pd.DataFrame(
                results
            )


            accuracy = (
                results_df["Correct"].mean()
                * 100
            )


            st.metric(
                "Model Accuracy",
                f"{accuracy:.2f}%"
            )


            st.dataframe(
                results_df,
                use_container_width=True
            )


            st.download_button(
                "⬇️ Download Backtest Results",
                results_df.to_csv(
                    index=False
                ),
                "virtual_oracle_backtest.csv",
                "text/csv"
            )


# =====================================================
# SCREENSHOT
# =====================================================

with tabs[2]:

    st.subheader(
        "📷 SportyBet Screenshot"
    )

    st.write(
        "Upload a screenshot of your virtual football slip."
    )


    screenshot = st.file_uploader(
        "Upload PNG/JPG",
        type=[
            "png",
            "jpg",
            "jpeg"
        ],
        key="screenshot"
    )


    if screenshot:

        st.image(
            screenshot,
            use_container_width=True
        )


        st.warning(
            "OCR is the next module. "
            "The current version displays the screenshot "
            "but does not automatically read it yet."
        )


# =====================================================
# DATA
# =====================================================

with tabs[3]:

    st.subheader(
        "📚 Historical Data Format"
    )

    st.write(
        "Your CSV should look like this:"
    )


    st.code(
"""home,away,h2h_home,home_form,away_form,over_rate,draw_rate,actual
Team A,Team B,0.55,0.60,0.45,0.55,0.25,HOME
Team C,Team D,0.40,0.45,0.60,0.50,0.30,AWAY""",
        language="csv"
    )


# =====================================================
# ABOUT
# =====================================================

with tabs[4]:

    st.subheader(
        "ℹ️ About Virtual Oracle"
    )

    st.write(
        """
Virtual Oracle is a personal statistical research
tool designed to test virtual-football prediction
ideas against historical results.

The goal is to collect data, test models and measure
actual performance rather than rely on unsupported
claims of guaranteed predictions.
"""
    )


    st.warning(
        "Virtual sports can be generated by random-number "
        "generators or algorithmic systems. Historical patterns "
        "do not guarantee future outcomes."
    )


    st.markdown("""
### Development Roadmap

✅ Prediction interface

✅ Probability model

✅ CSV backtesting

✅ Screenshot upload

⬜ Automatic OCR

⬜ Historical result database

⬜ Automatic result collection

⬜ Advanced prediction model

⬜ Prediction history

⬜ Admin dashboard

⬜ User accounts
""")
