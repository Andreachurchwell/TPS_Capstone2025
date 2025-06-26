# Week 11 Reflection

## 🔖 Section 0: Fellow Details

| Field               | Your Entry                       |
|---------------------|----------------------------------|
| **Name**            | Andrea Churchwell                |
| **GitHub Username** | andreachurchwell                 |
| **Preferred Track** | undecided                        |
| **Team Interest**   | totally                          |

---


✍️ Section 1: Week 11 Reflection
Key Takeaways

I actually started messing around with the project a few weeks ago just to get ahead and give it my best shot

I ended up building something that looked really cool — I was proud of it

Then I found out we had to break everything into separate modules and folders, and that hit hard at first

It felt like a big setback, but I’m finally starting to make progress now

I realized this project is supposed to be fun and help us practice everything we’ve learned, not make us miserable

Concept Connections

I feel more confident working with APIs and getting JSON data into the GUI

I’ve learned a ton about styling and organizing Tkinter widgets

Still working on: separating code into multiple files, importing cleanly, and handling errors the “right” way

Starting to see how much we’ve learned across the past 10 weeks — it’s a lot

Early Challenges

Breaking up my code into folders felt like a nightmare at first

I was honestly in a bad mood for a few days because of all the confusion

I finally decided to stop stressing, let go a little, and just play with it again


Support Strategies

I’m leaning on office hours when I feel lost

ChatGPT has been a lifesaver for sorting out imports and structure

I'm reminding myself it’s okay to use AI and that struggling is part of learning

Watching others build and asking questions helps me stay motivated





🧠 Section 2: Feature Selection Rationale
#	Feature Name	Difficulty	Why You Chose It / Learning Goal
Weather Icons	        1	    I love visuals, and this helps make the app feel fun and polished
Theme Switcher	        2	    I wanted to challenge myself to figure out how to toggle styles in a Tkinter app
Interactive Map	        2	    I thought it was really cool to show the city on a live map — it makes it feel real
Next Two Day Guess	    3	    This one pushes me — it’s my stretch goal to try out a bit of prediction logic, plus it knocks out the 7 day too!!
Saving Data Into CSV    1
Matplotlib Charts       1


🗂️ Section 3: High-Level Architecture Sketch
Folder + Module Outline
*** as of now: this will change some more than likely ***
weather_app/
│
├── app.py                  # Main app launcher
├── .env                    # Stores API key (not committed)
│
├── /core/                  # Main logic
│   ├── api.py              # Handles API calls to OpenWeather
│   ├── storage.py          # Saves CSV data
│   ├── icons.py            # Loads weather icons from the web
│
├── /features/              # Extra features
│   ├── dark_light_mode.py  # Light/dark theme toggle
│   ├── forecast.py         # 5-day forecast display
│   ├── map_feature.py      # Displays city location on map
│   ├── guess_weather.py    # Tomorrow’s weather prediction (stretch feature)
│
├── /gui/                   # GUI layout
│   └── main_window.py      # MainWindow class and all UI layout
│
├── /data/                  # Local data files like history.txt or csvs
└── README.md



📊 Section 4: Data Model Plan


File/Table Name	          Format	Example Row
weather_history.txt	      txt	2025-06-09,Selmer,96°F,Partly Cloudy
forecast_data.csv	      csv	2025-06-10,Selmer,High: 97,Low: 72,Cloudy
guess_results.csv	      csv	Selmer,2025-06-11,Predicted: Rain,Accuracy: 66%
map_location.json	      json	{ "city": "Selmer", "lat": 35.1706, "lon": -88.5948 }

📆 Section 5: Personal Project Timeline (Weeks 12–17)
*** Honestly, this is a very rough draft ***

| Week | Monday              | Tuesday           | Wednesday        | Thursday          | Key Milestone                 |
| ---- | ------------------- | ----------------- | ---------------- | ----------------- | ----------------------------- |
| 12   | API setup ✅         | Error handling ✅  | Built base UI ✅  | Started cleanup   | Core app already running ✅    |
| 13   | Add weather icons   | Refactor forecast | Forecast visuals | Style tweaks      | Feature 1 + forecast polished |
| 14   | Map view in place   | Test city pins    | Improve layout   | Smooth scrolling  | Map feature complete          |
| 15   | Theme switcher work | Add toggles       | Test light mode  | Debug UI flickers | Theme switcher done           |
| 16   | Tomorrow’s Guess    | Cleanup extras    | Final testing    | Export CSV review | All features + enhancement    |
| 17   | Polish and rehearse | Buffer if needed  | 🎉 Demo Day      | —                 | Ready to show off!            |



⚠️ Section 6: Risk Assessment
*** wasn't sure on what to say here, so i ask chat...now im stressing! ***

Risk	                     Likelihood	               Impact	           Mitigation Plan
API Rate Limit	              Medium	               Medium	     Add a delay or cache the last call so it’s not hitting too often
Breaking app with refactors	  Medium	               High	Test     each feature in isolation before plugging into the full app
Theme switcher bugs UI flow	   Low	                   Medium	     Keep theme logic simple and test on a small section first
Forecast layout getting messy	Medium	               Medium	     Use frames and scroll widgets to keep things clean
Getting stuck on enhancement	Medium	               Low	         Ask for help early and be okay scaling it down if needed