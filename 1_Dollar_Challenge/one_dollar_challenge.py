import streamlit as st  # 📦 Import Streamlit for creating the app interface
from datetime import datetime  # 📅 Import datetime module for handling date and time
from fpdf import FPDF  # 🖨️ Import FPDF for generating PDF files
import random  # 🎲 Import random for generating random quotes
import json  # 🗃️ Import json to handle JSON data
import requests  # 🌐 Import requests to make HTTP requests
from io import BytesIO  # 🧳 Import BytesIO to handle byte data
import base64  # 🔐 Import base64 for encoding the animations

# 🧠 Load Lottie from URL
def load_lottieurl(url: str):  # 📥 Define a function to load Lottie animation from URL
    r = requests.get(url)  # 🌍 Get the animation from the URL
    if r.status_code != 200:  # ❌ Check if request was successful
        return None  # 🚫 Return None if the request failed
    return r.json()  # ✅ Return the JSON data of the animation

# ✅ Load Animations
goal_animation = load_lottieurl("https://lottie.host/89b54be7-6c88-403f-bb0a-d78b67e9c18a/1GeXgnz9ZX.json")  # 🎯 Load goal animation
footer_animation = load_lottieurl("https://lottie.host/bd0d3596-3306-4c2c-8b2d-0b0d8321d8fb/wbP98C0zRW.json")  # 🔽 Load footer animation
button_animation = load_lottieurl("https://lottie.host/c02d61cf-b113-4b7d-9628-c96ae0a3e04e/csXqIzIGMv.json")  # ⏩ Load button animation
start_animation = load_lottieurl("https://lottie.host/470760fd-2b11-463f-9b6a-8b4fc365b75b/WOfbwWzJdd.json")  # 🚀 Load start animation
motivation_animation = load_lottieurl("https://lottie.host/5ad80e4f-285e-4f0e-9b2f-e9394cf1dca1/bJ6TMIK8zB.json")  # 💪 Load motivation animation

# 🎞️ Display Lottie
def st_lottie(lottie_json, height=300, key=None):  # 📺 Define a function to display Lottie animation
    if lottie_json:  # ✅ Check if Lottie JSON exists
        b64_json = base64.b64encode(json.dumps(lottie_json).encode()).decode()  # 🔐 Convert JSON to base64
        st.components.v1.html(  # 💻 Render HTML component in Streamlit
            f"""
            <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
            <lottie-player src="data:application/json;base64,{b64_json}" background="transparent" speed="1" style="width: 100%; height: {height}px;" loop autoplay></lottie-player>
            """,  # 🎞️ Embed Lottie animation in the HTML
            height=height,  # 📏 Set height for the animation
            key=key,  # 🔑 Assign a unique key for the animation
        )

# 📚 Goal Manager
class GoalManager:  # 🛠️ Define the GoalManager class for managing goals
    def __init__(self):  # 🧑‍💻 Initialize the GoalManager
        if "goals" not in st.session_state:  # ❗ Check if goals exist in session state
            st.session_state.goals = []  # ➖ Initialize an empty list for goals
            st.session_state.completed = 0  # ➖ Initialize completed goals counter
            st.session_state.streak = 0  # ➖ Initialize streak counter

    def add_goal(self, title, deadline):  # ✍️ Define function to add a new goal
        st.session_state.goals.append({  # ➕ Add a new goal to the list
            "title": title,  # 📝 Goal title
            "deadline": deadline,  # 📅 Deadline for the goal
            "created_at": datetime.now().strftime("%Y-%m-%d"),  # 🕓 Created date of the goal
            "completed": False  # ❌ Mark goal as incomplete initially
        })

    def complete_goal(self, index):  # ✅ Define function to mark a goal as completed
        st.session_state.goals[index]["completed"] = True  # ✅ Set goal as completed
        st.session_state.completed += 1  # ➕ Increment completed goals count
        st.session_state.streak += 1  # ➕ Increment streak count

    def reset_goals(self):  # 🔄 Define function to reset all goals
        st.session_state.goals = []  # 🧹 Clear all goals
        st.session_state.completed = 0  # 🧹 Reset completed goals count
        st.session_state.streak = 0  # 🧹 Reset streak count

    def export_goals_to_pdf(self):  # 📄 Define function to export goals to a PDF
        pdf = FPDF()  # 🖨️ Create a new PDF document
        pdf.add_page()  # ➕ Add a page to the PDF
        pdf.set_font("Arial", 'B', 16)  # 🖋️ Set font style
        pdf.cell(200, 10, txt="Your Goals Report", ln=True, align='C')  # 📃 Add title to PDF
        pdf.ln(10)  # 🔲 Add space in PDF
        pdf.set_font("Arial", size=12)  # 🖋️ Set font size
        for goal in st.session_state.goals:  # 📄 Loop through all goals
            status = "Completed" if goal["completed"] else "Pending"  # ✅/❌ Set goal status
            pdf.multi_cell(0, 10, f"Title: {goal['title']}\nStatus: {status}\nDeadline: {goal['deadline']}\nCreated At: {goal['created_at']}\n")  # 📝 Add goal details to PDF
            pdf.ln(5)  # 🔲 Add space between goal entries
        pdf_output = BytesIO()  # 🧳 Prepare PDF data for output
        pdf_bytes = pdf.output(dest='S').encode('latin1')  # 🖨️ Get the PDF as bytes
        pdf_output.write(pdf_bytes)  # ➕ Write the bytes to the output
        pdf_output.seek(0)  # 🔁 Seek to the beginning of the output
        return pdf_output  # 📥 Return the PDF output

# 🧾 Header
def show_header():  # 📝 Define function to show the header
    st.markdown("<h1 style='text-align: center; color: #00C896;'>🌟 Smart Goal Master 🌟</h1>", unsafe_allow_html=True)  # 📑 Add header with title
    st_lottie(start_animation, height=300, key="start_anim")  # 🎞️ Show start animation
    st.markdown("---")  # ➖ Add a horizontal line for separation

# 👣 Footer
def show_footer():  # 📝 Define function to show the footer
    st.markdown(  # 📑 Add footer text
        "<div style='text-align: center; font-size: 16px;'>"
        "Made with ❤️ by <b>MUHAMMAD HAMMAD ZUBAIR</b> 👨‍💻<br>"
        "Powered by <span style='color: #FF4B4B;'>Python</span> 🐍 & <span style='color: #4F8BF9;'>Streamlit</span> 🚀"
        "</div>",
        unsafe_allow_html=True  # ✅ Allow HTML in the footer
    )

# 💬 Motivation Quote
def get_random_quote():  # 📜 Define function to get a random motivational quote
    quotes = [  # 📋 List of motivational quotes
        "💡 Believe in yourself — You’re halfway there!",
        "🚀 Make it happen, shock everyone!",
        "🔥 Focus + Consistency = Success",
        "🎯 Stay on track — great things take time!",
    ]
    return random.choice(quotes)  # 🎲 Return a random quote

# 🚀 Main App
def main():  # 🧑‍💻 Define the main function
    st.set_page_config(page_title="Smart Goal Master", page_icon="🌟", layout="centered")  # 📜 Set page configuration
    show_header()  # 📝 Show header
    manager = GoalManager()  # 🛠️ Initialize the GoalManager

    with st.sidebar:  # 🔲 Create a sidebar
        st.title("📌 Menu")  # 📋 Set the title of the sidebar
        choice = st.radio("Select Option", ["➕ Add Goal", "📋 View Goals", "📄 Export Goals", "🧹 Reset All"])  # 📊 Display radio buttons for menu

    if choice == "➕ Add Goal":  # 📥 If the user chooses to add a goal
        st.subheader("✨ Add a New Goal")  # 📝 Show subheading
        st_lottie(goal_animation, height=200, key="goal_anim")  # 🎞️ Show goal animation
        title = st.text_input("🎯 Goal Title")  # ✍️ Ask for goal title
        deadline = st.date_input("📅 Deadline")  # 📅 Ask for goal deadline
        if st.button("✅ Add Goal"):  # ✅ If the add goal button is clicked
            if title:  # ✅ If title is provided
                manager.add_goal(title, deadline)  # ➕ Add the goal
                st.success("Goal added successfully! 🚀")  # ✅ Show success message
                st.balloons()  # 🎈 Show balloons animation
                st_lottie(motivation_animation, height=250, key="after_add_goal")  # 🎞️ Show motivation animation after adding goal
            else:  # ❌ If title is missing
                st.warning("⚠️ Title required!")  # ⚠️ Show warning message

    elif choice == "📋 View Goals":  # 📋 If the user chooses to view goals
        st.subheader("📋 Your Goals")  # 📑 Show subheading
        st_lottie(goal_animation, height=150, key="view_anim")  # 🎞️ Show goal animation
        if st.session_state.goals:  # ✅ If there are any goals
            for idx, goal in enumerate(st.session_state.goals):  # 🧑‍💻 Loop through goals
                st.markdown(f"""
                - **{goal['title']}**  # 📝 Display goal title
                  - Deadline: `{goal['deadline']}`  # 📅 Show goal deadline
                  - Status: {'✅ Completed' if goal['completed'] else '❌ Pending'}  # ✅/❌ Show goal status
                """)
                if not goal["completed"]:  # ❌ If the goal is not completed
                    if st.button(f"✅ Mark Completed - Goal {idx+1}"):# ✅ If the user wants to mark as complete
                        manager.complete_goal(idx)  # ✅ Mark the goal as complete
                        st.success("🎉 Marked as completed!")  # ✅ Show success message
                        st.balloons()  # 🎈 Show balloons animation
                        st_lottie(button_animation, height=150, key=f"done_{idx}")  # 🎞️ Show button animation
        else:  # ❌ If no goals are found
            st.info("🚧 No goals found. Add some goals to begin.")  # 🧑‍💻 Show info message
            st_lottie(motivation_animation, height=200, key="empty_view")  # 🎞️ Show motivation animation

        st.markdown("### 📈 Progress")  # 📊 Show progress heading
        if st.session_state.goals:  # ✅ If there are goals
            total = len(st.session_state.goals)  # 🔢 Get total goals
            completed = st.session_state.completed  # 🔢 Get completed goals
            progress = int((completed / total) * 100)  # 📊 Calculate progress percentage
            st.progress(progress)  # 📊 Show progress bar
            st.info(f"✔ {completed}/{total} goals completed.")  # ✅ Show progress info
            if completed >= 5:  # 🏆 If 5 or more goals are completed
                st.success("🏆 Super Achiever! Keep going!")  # 🎉 Show success message
                st_lottie(motivation_animation, height=200, key="badge_reward")  # 🎞️ Show badge animation
            st.info(f"🔥 Streak: {st.session_state.streak}")  # 🔥 Show streak count

        st.markdown("### 💬 Boost of Motivation")  # 💪 Show motivational quotes heading
        st.info(get_random_quote())  # 📜 Show random motivational quote

    elif choice == "📄 Export Goals":  # 📤 If the user chooses to export goals
        st.subheader("📤 Export Goals")  # 📑 Show export goals subheading
        pdf_file = manager.export_goals_to_pdf()  # 📄 Export goals to PDF
        st.download_button("📄 Download PDF", data=pdf_file, file_name="goals_report.pdf", mime="application/pdf")  # 📥 Allow PDF download
        st.success("✅ Your goals have been exported.")  # ✅ Show success message
        st_lottie(button_animation, height=200, key="export_anim")  # 🎞️ Show export animation

    elif choice == "🧹 Reset All":  # 🔄 If the user chooses to reset all goals
        st.subheader("⚡ Reset Everything")  # ⚡ Show reset subheading
        if st.button("🔄 Confirm Reset"):  # 🔄 If the reset button is clicked
            manager.reset_goals()  # 🧹 Reset all goals
            st.success("🧹 All goals cleared!")  # ✅ Show success message
            st.snow()  # ❄️ Show snow animation
            st_lottie(button_animation, height=200, key="reset_anim")  # 🎞️ Show reset animation

    show_footer()  # 📑 Show footer

if __name__ == "__main__":  # 🧑‍💻 If the script is executed
    main()  # 🚀 Run the main app function
