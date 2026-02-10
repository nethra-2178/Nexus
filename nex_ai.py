import customtkinter as ctk
import sqlite3
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nexbot.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nex_details(
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Age INTEGER,
            Height REAL,
            Weight REAL,
            Gender TEXT,
            BP_Systolic INTEGER,
            BP_Diastolic INTEGER,
            Blood_Sugar REAL,
            Cholesterol REAL,
            Heart_Rate INTEGER,
            Timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

BP_RANGES = [
    {"sys": (0, 50), "dia": (0, 33), "label": "Dangerously Low", "color": "Dark Red", "advice": "Seek medical attention immediately"},
    {"sys": (51, 59), "dia": (34, 39), "label": "Too Low", "color": "Red", "advice": "Consult doctor"},
    {"sys": (60, 89), "dia": (40, 59), "label": "Low", "color": "Orange", "advice": "Monitor and rest"},
    {"sys": (90, 119), "dia": (60, 79), "label": "Normal", "color": "Green", "advice": "Keep up the good habits"},
    {"sys": (120, 129), "dia": (0, 79), "label": "Elevated", "color": "Yellow", "advice": "Monitor lifestyle"},
    {"sys": (130, 139), "dia": (80, 89), "label": "Hypertension Stage 1", "color": "Orange", "advice": "Consult doctor"},
    {"sys": (140, 179), "dia": (90, 119), "label": "Hypertension Stage 2", "color": "Red", "advice": "Medical attention needed"},
    {"sys": (180, 300), "dia": (120, 300), "label": "Hypertensive Crisis", "color": "Dark Red", "advice": "Seek emergency medical care"},
]

GLUCOSE_RANGES = [
    {"mgdl": (315, 1000), "label": "Danger-High", "advice": "Medical attention needed"},
    {"mgdl": (280, 314), "label": "High", "advice": "Medical attention needed"},
    {"mgdl": (250, 279), "label": "High", "advice": "Medical attention needed"},
    {"mgdl": (215, 249), "label": "High", "advice": "Medical attention needed"},
    {"mgdl": (180, 214), "label": "Borderline", "advice": "Consult doctor"},
    {"mgdl": (150, 179), "label": "Borderline", "advice": "Consult doctor"},
    {"mgdl": (120, 149), "label": "Borderline", "advice": "Consult doctor"},
    {"mgdl": (108, 119), "label": "Normal", "advice": "No action needed"},
    {"mgdl": (72, 107), "label": "Normal", "advice": "No action needed"},
    {"mgdl": (50, 71), "label": "Low", "advice": "Consult doctor"},
]

CHOLESTEROL_RANGES = [
    {"total": (240, 1000), "ldl": (160, 1000), "hdl_m": (0, 39), "hdl_f": (0, 49), "label": "Dangerous", "advice": "Seek medical attention"},
    {"total": (200, 239), "ldl": (100, 159), "hdl_m": (40, 59), "hdl_f": (50, 59), "label": "At-risk", "advice": "Monitor diet and exercise"},
    {"total": (0, 199), "ldl": (0, 99), "hdl_m": (60, 1000), "hdl_f": (60, 1000), "label": "Heart-healthy", "advice": "Keep healthy lifestyle"},
]

HEART_RATE_RESTING = [
    {"age": (18, 25), "male": (62, 73), "female": (64, 80)},
    {"age": (26, 35), "male": (62, 73), "female": (64, 81)},
    {"age": (36, 45), "male": (63, 75), "female": (65, 82)},
    {"age": (46, 55), "male": (64, 76), "female": (66, 83)},
    {"age": (56, 65), "male": (62, 75), "female": (64, 82)},
    {"age": (66, 120), "male": (62, 73), "female": (64, 81)},
]

HEART_RATE_EFFORT = [
    {"range": (171, 190), "effort": "Very Hard", "percent": "90-100%", "zone": "Performance Redline Zone", "effect": "Develops maximum capacity"},
    {"range": (152, 171), "effort": "Hard", "percent": "80-90%", "zone": "Threshold Zone", "effect": "Increases maximum capacity"},
    {"range": (133, 152), "effort": "Moderate", "percent": "70-80%", "zone": "Aerobic Zone", "effect": "Improves aerobic fitness"},
    {"range": (114, 133), "effort": "Light", "percent": "60-70%", "zone": "Temperate Zone", "effect": "Improves basic endurance"},
    {"range": (95, 114), "effort": "Very Light", "percent": "50-60%", "zone": "Healthy Heart Zone", "effect": "Improves overall health"},
]

MEDICAL_DICTIONARY = {
    "hypertension": "High blood pressure. Your heart is working harder than it should.",
    "cholesterol": "A fat in your blood. Too much can clog arteries and harm your heart.",
    "systolic": "The top number in your blood pressure. It shows how hard your heart is pumping.",
    "diastolic": "The bottom number in your blood pressure. It shows the pressure when your heart rests.",
    "tachycardia": "A very fast heartbeat. Could happen after exercise or sometimes needs checking.",
    "bradycardia": "A very slow heartbeat. Might be normal in fit people, but sometimes needs attention.",
    "glucose": "Blood sugar. Your body uses it for energy.",
    "diabetes": "When your body has trouble controlling blood sugar levels.",
    "resting heart rate": "How fast your heart beats when you are relaxed and calm.",
    "borderline": "Something is a little higher or lower than normal, keep an eye on it.",
    "normal": "Everything is in a healthy range, nothing to worry about.",
    "dangerous": "This is risky and may need medical help quickly.",
    "hypertensive crisis": "Extremely high blood pressure. This is an emergency, seek help fast.",
    "low blood sugar": "Your blood sugar is too low. You may feel dizzy or weak.",
    "high blood sugar": "Your blood sugar is high. Could be a sign of diabetes or stress.",
    "heart-healthy": "Your heart is in good shape, keep doing what you’re doing!",
    "at-risk": "Your heart or blood values are a bit off. Watch your diet and habits.",
    "cholesterol plaque": "Fatty build-up in your arteries. Can block blood flow if too much.",
    "stroke": "When blood flow to the brain is blocked. Can cause serious problems if not treated fast.",
    "heart attack": "When blood flow to the heart is blocked. Emergency! Call help immediately.",
    "dehydration": "Not enough water in your body. Can make you tired or dizzy.",
    "BMI": "Body Mass Index. A simple number to check if your weight is healthy for your height.",
    "aerobic exercise": "Activity like walking, running, or swimming that makes your heart and lungs stronger.",
    "anaerobic exercise": "Short, intense activity like sprinting or lifting weights that builds strength.",
}

def predict_health_risks(age, gender, bp_sys, bp_dia, sugar, cholesterol, hr):
        """
        #Analyze user data and provide risk predictions for BP, glucose, cholesterol, and heart rate.
        #Returns a human-friendly summary with advice.
        """
        risks = []

        # Blood Pressure
        bp_label = None
        for r in BP_RANGES:
            if r["sys"][0] <= bp_sys <= r["sys"][1] and r["dia"][0] <= bp_dia <= r["dia"][1]:
                bp_label = r["label"]
                break
        if bp_label in ["Hypertension Stage 1", "Hypertension Stage 2", "Elevated", "Hypertensive Crisis"]:
            risks.append(f"Your blood pressure is **{bp_sys}/{bp_dia} mmHg ({bp_label})** — {r['advice']}")
        elif bp_label in ["Low", "Too Low", "Dangerously Low"]:
            risks.append(f"Your blood pressure is **{bp_sys}/{bp_dia} mmHg ({bp_label})** — {r['advice']}")

        # Glucose
        glucose_label = None
        for r in GLUCOSE_RANGES:
            low, high = r["mgdl"]
            if low <= sugar <= high:
                glucose_label = r["label"]
                glucose_advice = r["advice"]
                break
        if glucose_label in ["High", "Danger-High", "Low"]:
            risks.append(f"Blood sugar **{sugar} mg/dL ({glucose_label})** — {glucose_advice}")

        # Cholesterol
        chol_label = None
        for r in CHOLESTEROL_RANGES:
            t_low, t_high = r["total"]
            if t_low <= cholesterol <= t_high:
                chol_label = r["label"]
                chol_advice = r["advice"]
                break
        if chol_label in ["At-risk", "Dangerous"]:
            risks.append(f"Cholesterol level **{cholesterol} mg/dL ({chol_label})** — {chol_advice}")

        # Heart Rate
        resting_low = resting_high = None
        for r in HEART_RATE_RESTING:
            if r["age"][0] <= age <= r["age"][1]:
                if gender.lower() == "female":
                    resting_low, resting_high = r["female"]
                else:
                    resting_low, resting_high = r["male"]
                break
        if resting_low is not None:
            if hr < resting_low:
                risks.append(f"Resting heart rate **{hr} bpm** is lower than typical ({resting_low}-{resting_high} bpm)")
            elif hr > resting_high:
                risks.append(f"Resting heart rate **{hr} bpm** is higher than typical ({resting_low}-{resting_high} bpm)")

        if not risks:
            return "Based on your data, there are no major risks detected right now. Keep up the healthy habits 💚"
        else:
            return "Here are some health risks I noticed:\n" + "\n".join(risks)


# Main App Class
class NexBot(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nexus")
        self.geometry("900x550")
        self.resizable(True, True)
        ctk.set_appearance_mode("light")    
        self.show_welcome_screen()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear()
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill='both')

        self.welcome_label = ctk.CTkLabel(frame, text="Welcome to Nexus", font=("Times New Roman", 30, "bold", "italic"))
        self.welcome_label.pack(pady=40)

        self.type_text_animation("Hi, I'm Nexus.\nYour personal Healthcare Companion🤍")


        continue_btn = ctk.CTkButton(frame, text="Continue →", width=200, command=self.user_registration)
        continue_btn.pack(pady=60)

    def type_text_animation(self, text, index=0):
        if index <= len(text):
            self.welcome_label.configure(text=text[:index])
            self.after(30, self.type_text_animation, text, index + 1)

    def user_registration(self):
        self.clear()
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both")

        ctk.CTkLabel(frame, text="User Registration",
                     font=("Times New Roman", 30, "bold")).pack(pady=30)

        name = ctk.CTkEntry(frame, placeholder_text="Name")
        age = ctk.CTkEntry(frame, placeholder_text="Age")
        height = ctk.CTkEntry(frame, placeholder_text="Height (in cm)")
        weight = ctk.CTkEntry(frame, placeholder_text="Weight (in kg)")
        gender = ctk.CTkEntry(frame, placeholder_text="Gender")
        bp_systolic = ctk.CTkEntry(frame, placeholder_text="Blood Pressure Systolic")
        bp_diastolic = ctk.CTkEntry(frame, placeholder_text="Blood Pressure Diastolic")
        blood_sugar = ctk.CTkEntry(frame, placeholder_text="Blood Sugar Level")
        cholesterol = ctk.CTkEntry(frame, placeholder_text="Cholesterol Level")
        heart_rate = ctk.CTkEntry(frame, placeholder_text="Heart Rate")        

        for e in (name, age, height, weight, gender, bp_systolic, bp_diastolic, blood_sugar, cholesterol, heart_rate):
            e.pack(pady=8)

        def submit():
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO nex_details (Name, Age, Height, Weight, Gender, BP_Systolic, BP_Diastolic, Blood_Sugar, Cholesterol, Heart_Rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name.get(), age.get(), height.get(), weight.get(), gender.get(), bp_systolic.get(), bp_diastolic.get(), blood_sugar.get(), cholesterol.get(), heart_rate.get()))
            conn.commit()
            did = cursor.lastrowid
            conn.close()
            self.nex_bot(did, name.get())

        ctk.CTkButton(frame, text="Register", command=submit).pack(pady=25)

    def nex_bot(self, did, name):
        self.clear()

        # Main frame
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both")

        # Welcome message at top
        ctk.CTkLabel(
            frame,
            text=f"Hi {name} I'm Nexus.\nAsk me anything about your health data.",
            font=("Times New Roman", 28, "bold"),
            justify="center"
        ).pack(pady=20)

        self.chat_box = ctk.CTkTextbox(frame, width=900, height=500)
        self.chat_box.pack(pady=10)
        self.chat_box.insert("end", "Nexus : Hi.....I'm Nexus. And I'm here to help you so that you could understand your health better.\n\n")
        self.chat_box.configure(state="disabled")  # Make it read-only

        self.user_input = ctk.CTkEntry(frame, placeholder_text="Ask anything")
        self.user_input.pack(fill="x", padx=40, pady=10)

        self.user_input.bind(
            "<Return>",
            lambda event: self.handle_message(did)
        )

        send_btn = ctk.CTkButton(
            frame,
            text="Send",
            command=lambda: self.handle_message(did)
        )
        send_btn.pack(pady=10)

    def get_user_data(self, user_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nex_details WHERE User_ID=?", (user_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def handle_message(self, user_id):
        msg = self.user_input.get().strip()
        if not msg:
            return

        self.user_input.delete(0, "end")

        # Enable chat box
        self.chat_box.configure(state="normal")

        # Show USER message
        self.chat_box.insert("end", f"You : {msg}\n")

        # Generate bot response
        response = self.respond(user_id, msg)
        # Show BOT message
        self.chat_box.insert("end", f"Nexus : {response}\n\n")

        # Disable chat box again
        self.chat_box.configure(state="disabled")

        # Auto-scroll
        self.chat_box.yview("end")


    def respond(self, user_id, msg):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nex_details WHERE User_ID=?", (user_id,))
        data = cursor.fetchone()
        conn.close()

        if not data:
            return "I couldn't find your health data"

        # Get user data
        age = int(data[2])
        gender = (data[5] or "").lower()
        bp_sys = int(data[6])
        bp_dia = int(data[7])
        sugar = float(data[8])
        cholesterol = float(data[9])
        hr = int(data[10])

        msg = msg.lower()

        #Blood pressure
        if any(word in msg for word in ["blood pressure", "bp", "systole", "diastole", "hypertension", "hypotension"]):
            for r in BP_RANGES:
                if r["sys"][0] <= bp_sys <= r["sys"][1] and r["dia"][0] <= bp_dia <= r["dia"][1]:
                    return (
                        f"Your blood pressure is {bp_sys}/{bp_dia} mmHg.\n"
                        f"That falls under **{r['label']}** {r['color']}.\n"
                        f"{r['advice']} 🤍"
        )
        
        #Heart rate
        if any(word in msg for word in ["heart rate", "heartrate", "pulse", "cardiac", "bpm", "rbpm"]):
            resting_low = resting_high = None

            # Find resting range by age & gender
            for r in HEART_RATE_RESTING:
                if r["age"][0] <= age <= r["age"][1]:
                    if gender == "female":
                        resting_low, resting_high = r["female"]
                    else:
                        resting_low, resting_high = r["male"]
                    break

            if resting_low is None:
                status = "hard to interpret"
            elif hr < resting_low:
                status = "lower than typical resting levels"
            elif hr > resting_high:
                status = "higher than typical resting levels"
            else:
                status = "within a healthy resting range"

            effort_info = None
            for e in HEART_RATE_EFFORT:
                if e["range"][0] <= hr <= e["range"][1]:
                    effort_info = e
                    break

            responses = []

            responses.append(
                f"Your heart rate is **{hr} bpm**.\n"
                f"For your age and gender, that’s **{status}**.\n"
                f"If this was measured at rest and you feel fine, there’s usually no immediate concern"
            )

            if effort_info:
                responses.append(
                    f"Your heart rate is **{hr} bpm**.\n"
                    f"This falls into the **{effort_info['zone']}** ({effort_info['percent']}).\n"
                    f"Effort level: **{effort_info['effort']}** — {effort_info['effect']} "
                )

            responses.append(
                f"Quick pulse check\n"
                f"• Current rate: **{hr} bpm**\n"
                f"• Expected resting range: **{resting_low}–{resting_high} bpm**\n"
                f"• Interpretation: {status.capitalize()}"
            )

            return random.choice(responses)

        #Blood sugar
        if any(word in msg for word in ["sugar", "glucose", "diabetes"]):
            glucose_label = None
            glucose_advice = None

            for r in GLUCOSE_RANGES:
                low, high = r["mgdl"]
                if low <= sugar <= high:
                    glucose_label = r["label"]
                    glucose_advice = r["advice"]
                    break

            if glucose_label is None:
                return f"Your blood sugar is **{sugar} mg/dL**, but I’m unable to clearly classify it right now"

            sugar_responses = [
                f"Your blood sugar level is **{sugar} mg/dL**.\nThat falls under **{glucose_label}**.\n{glucose_advice} ",
                f"I checked your glucose reading — **{sugar} mg/dL**.\nThis is considered **{glucose_label}**.\n{glucose_advice}.",
                f"Here’s a quick blood sugar update\n• Reading: **{sugar} mg/dL**\n• Status: **{glucose_label}**\n• Advice: {glucose_advice}",
                f"Your glucose came in at **{sugar} mg/dL**.\nThis is classified as **{glucose_label}**.\nPlease keep this in mind: {glucose_advice} 🤍"
            ]

            return random.choice(sugar_responses)

        #Cholesterol
        if "cholesterol" in msg:
            chol_label = None
            chol_advice = None

            for r in CHOLESTEROL_RANGES:
                t_low, t_high = r["total"]
                if t_low <= cholesterol <= t_high:
                    chol_label = r["label"]
                    chol_advice = r["advice"]
                    break

            if chol_label is None:
                return (
                    f"Your cholesterol is **{cholesterol} mg/dL**, "
                    f"but I’m unable to clearly categorize it right now"
                )

            cholesterol_responses = [
                f"Your total cholesterol is **{cholesterol} mg/dL**.\n"
                f"This falls under **{chol_label}**.\n"
                f"{chol_advice} 🤍",
                f"I checked your cholesterol levels\n"
                f"• Total: **{cholesterol} mg/dL**\n"
                f"• Status: **{chol_label}**\n"
                f"• Advice: {chol_advice}",
                f"Here’s a quick cholesterol update\n"
                f"Your reading of **{cholesterol} mg/dL** is considered **{chol_label}**.\n"
                f"{chol_advice}.",
                f"Your cholesterol came in at **{cholesterol} mg/dL**.\n"
                f"This is classified as **{chol_label}**.\n"
                f"Take note: {chol_advice} 🤍"
            ]

            return random.choice(cholesterol_responses)

        #Summarize
        if "summary" in msg or "overview" in msg:
            points = []
            improvements = []

            summary = "Here’s your health summary: \n\n"

            #blood pressure
            bp_label = None
            for r in BP_RANGES:
                if r["sys"][0] <= bp_sys <= r["sys"][1] and r["dia"][0] <= bp_dia <= r["dia"][1]:
                    bp_label = r["label"]
                    break
            if bp_label == "Normal":
                points.append("Your blood pressure is in a healthy range")
            elif bp_label in ["Low"]:
                improvements.append("Your blood pressure is lower than ideal")
            elif bp_label in ["Too Low"]:
                improvements.append("Your blood pressure is very low and should be monitored")
            elif bp_label in ["Dangerously Low"]:
                improvements.append("Your blood pressure is dangerously low and requires immediate medical attention")
            else:
                improvements.append("Your blood pressure is elevated")

            #heart
            resting_low = resting_high = None
            for r in HEART_RATE_RESTING:
                if r["age"][0] <= age <= r["age"][1]:
                    if gender == "female":
                        resting_low, resting_high = r["female"]
                    else:
                        resting_low, resting_high = r["male"]
                    break

            if resting_low is not None:
                if resting_low <= hr <= resting_high:
                    points.append("Your resting heart rate is healthy for your age and gender")
                elif hr < resting_low:
                    improvements.append("Your heart rate is lower than typical resting levels")
                else:
                    improvements.append("Your heart rate is higher than expected at rest")

            #glucose
            glucose_label = None
            for r in GLUCOSE_RANGES:
                low, high = r["mgdl"]
                if low <= sugar <= high:
                    glucose_label = r["label"]
                    break

            if glucose_label == "Normal":
                points.append("Your blood sugar levels are within a healthy range")
            elif glucose_label == "Borderline":
                improvements.append("Your blood sugar is borderline and should be monitored closely")
            elif glucose_label == "Low":
                improvements.append("Your blood sugar is low and may need medical attention")
            elif glucose_label in ["High"]:
                improvements.append("Your blood sugar is high and requires medical attention")
            elif glucose_label in ["Danger-High"]:
                improvements.append("Your blood sugar is dangerously high and requires immediate medical attention")

            #cholesterol
            chol_label = None
            for r in CHOLESTEROL_RANGES:
                t_low, t_high = r["total"]
                if t_low <= cholesterol <= t_high:
                    chol_label = r["label"]
                    break

            if chol_label == "Heart-healthy":
                points.append("Your cholesterol levels are heart-healthy")
            elif chol_label == "At-risk":
                improvements.append("Your cholesterol levels are at-risk and should be monitored")
            elif chol_label == "Dangerous":
                improvements.append("Your cholesterol levels are dangerously high and need medical attention")

            #Summary
            if points:
                summary += "What’s looking good:\n"
                for p in points:
                    summary += f"• {p}\n"

            if improvements:
                summary += "\nWhat could improve:\n"
                for i in improvements:
                    summary += f"• {i}\n"

            summary += (
                "\nNothing here looks alarming right now.\n"
                "Small, consistent habits can make a big difference over time "
            )

            return summary
            
        #Medical dictionary
        if any(keyword in msg for keyword in ["meaning", "mean", "definition", "explain", "what is", "define"]):
            found_terms = []
            for term in MEDICAL_DICTIONARY:
                if term in msg:
                    found_terms.append(f"**{term.capitalize()}**: {MEDICAL_DICTIONARY[term]}")

            if found_terms:
                return "Here’s what the word means\n\n" + "\n\n".join(found_terms)
            else:
                return "I couldn't find a definition for that term "
            
        #Health risk predictor
        if any(word in msg for word in ["predict", "prediction", "risk", "estimate", "forecast"]):
            return predict_health_risks(age, gender, bp_sys, bp_dia, sugar, cholesterol, hr)

        return (
            "I can help with your medical data\n"
            "Just ask me"
        )
              
if __name__ == "__main__":
    init_db()
    app = NexBot()
    app.mainloop()

