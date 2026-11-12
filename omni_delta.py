
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime, timedelta
import calendar


# ============================================================
# OMNI DELTA ENGINE v6.0
# ============================================================

BG = "#06152E"
PANEL = "#0B2345"
PANEL2 = "#102D55"
BLUE = "#168BFF"
CYAN = "#42D9FF"
WHITE = "#FFFFFF"
MUTED = "#A9C5E8"
GREEN = "#4DFFB5"

FONT = "Segoe UI"


# ============================================================
# FESTIVAL LISTS
# ============================================================

INDIA_FESTIVALS = [
    "Diwali",
    "Holi",
    "Durga Puja / Navratri",
    "Ganesh Chaturthi",
    "Eid-ul-Fitr",
    "Eid-al-Adha",
    "Christmas",
    "Raksha Bandhan",
    "Krishna Janmashtami",
    "Maha Shivratri",
    "Makar Sankranti / Pongal / Bihu",
    "Onam",
    "Chhath Puja",
    "Vaisakhi",
    "Guru Nanak Gurpurab",
    "Buddha Purnima",
    "Mahavir Jayanti",
    "Karwa Chauth",
    "Ratha Yatra",
    "Dussehra (Vijayadashami)",
    "Independence Day (August 15)",
    "Republic Day (January 26)",
    "Gandhi Jayanti",
    "Losar (Tibetan New Year)",
    "Hornbill Festival"
]

USA_FESTIVALS = [
    "Independence Day (Fourth of July)",
    "Thanksgiving",
    "Christmas",
    "Halloween",
    "New Year's Eve / New Year's Day",
    "Memorial Day",
    "Labor Day",
    "Juneteenth",
    "Martin Luther King Jr. Day",
    "Super Bowl Sunday",
    "Mardi Gras",
    "St. Patrick's Day",
    "Easter",
    "Valentine's Day",
    "Mother's Day",
    "Father's Day",
    "Veterans Day",
    "Presidents' Day",
    "Columbus Day / Indigenous Peoples' Day",
    "Groundhog Day",
    "Cinco de Mayo",
    "Hanukkah",
    "Kwanzaa",
    "Coachella Valley Music and Arts Festival",
    "Burning Man"
]

FESTIVALS = (
    ["INDIA • " + name for name in INDIA_FESTIVALS]
    + ["USA • " + name for name in USA_FESTIVALS]
)


# ============================================================
# KNOWN MOVABLE FESTIVAL DATES
# Dates are local calendar dates for the listed year.
# Lunar dates may vary by regional calendar or moon sighting.
# ============================================================

MOVABLE_DATES = {
    2026: {
        "INDIA • Guru Nanak Gurpurab": (11, 24),
        "INDIA • Hornbill Festival": (12, 1),
        "INDIA • Christmas": (12, 25),
        "USA • Christmas": (12, 25),
        "USA • Thanksgiving": (11, 26),
        "USA • Hanukkah": (12, 4),
        "USA • Kwanzaa": (12, 26),
    },

    2027: {
        "INDIA • Maha Shivratri": (3, 6),
        "INDIA • Eid-ul-Fitr": (3, 10),
        "INDIA • Holi": (3, 22),
        "INDIA • Eid-al-Adha": (5, 17),
        "INDIA • Buddha Purnima": (5, 20),
        "INDIA • Ratha Yatra": (7, 5),
        "INDIA • Raksha Bandhan": (8, 17),
        "INDIA • Krishna Janmashtami": (8, 25),
        "INDIA • Ganesh Chaturthi": (9, 4),
        "INDIA • Onam": (9, 12),
        "INDIA • Durga Puja / Navratri": (10, 5),
        "INDIA • Dussehra (Vijayadashami)": (10, 9),
        "INDIA • Karwa Chauth": (10, 18),
        "INDIA • Diwali": (10, 29),
        "INDIA • Chhath Puja": (11, 4),
        "INDIA • Guru Nanak Gurpurab": (11, 14),
        "INDIA • Losar (Tibetan New Year)": (2, 7),
        "INDIA • Mahavir Jayanti": (4, 19),
        "INDIA • Makar Sankranti / Pongal / Bihu": (1, 15),
        "INDIA • Vaisakhi": (4, 14),
        "INDIA • Hornbill Festival": (12, 1),

        "USA • Hanukkah": (12, 25),
        "USA • Kwanzaa": (12, 26),
    }
}


# ============================================================
# DATE CALCULATIONS
# ============================================================

def nth_weekday(year, month, weekday, n):
    """Return the date of the nth weekday in a month.
    Monday = 0, Sunday = 6.
    """
    first_day = date(year, month, 1)
    offset = (weekday - first_day.weekday()) % 7
    day = 1 + offset + (n - 1) * 7
    return date(year, month, day)


def last_weekday(year, month, weekday):
    last_day = calendar.monthrange(year, month)[1]
    result = date(year, month, last_day)

    while result.weekday() != weekday:
        result -= timedelta(days=1)

    return result


def easter_date(year):
    """Gregorian Easter Sunday calculation."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451

    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1

    return date(year, month, day)


def us_festival_date(name, year):
    """Calculate recurring US dates."""

    if name == "USA • Thanksgiving":
        return nth_weekday(year, 11, 3, 4)

    if name == "USA • Memorial Day":
        return last_weekday(year, 5, 0)

    if name == "USA • Labor Day":
        return nth_weekday(year, 9, 0, 1)

    if name == "USA • Juneteenth":
        return date(year, 6, 19)

    if name == "USA • Martin Luther King Jr. Day":
        return nth_weekday(year, 1, 0, 3)

    if name == "USA • Presidents' Day":
        return nth_weekday(year, 2, 0, 3)

    if name == "USA • Columbus Day / Indigenous Peoples' Day":
        return nth_weekday(year, 10, 0, 2)

    if name == "USA • Mother's Day":
        return nth_weekday(year, 5, 6, 2)

    if name == "USA • Father's Day":
        return nth_weekday(year, 6, 6, 3)

    if name == "USA • Easter":
        return easter_date(year)

    if name == "USA • Mardi Gras":
        return easter_date(year) - timedelta(days=47)

    if name == "USA • Super Bowl Sunday":
        return nth_weekday(year, 2, 6, 2)

    return None


# ============================================================
# AUTOMATIC FESTIVAL DATE FINDER
# ============================================================

FIXED_DATES = {
    "INDIA • Christmas": (12, 25),
    "USA • Christmas": (12, 25),

    "INDIA • Independence Day (August 15)": (8, 15),
    "INDIA • Republic Day (January 26)": (1, 26),
    "INDIA • Gandhi Jayanti": (10, 2),

    "USA • Independence Day (Fourth of July)": (7, 4),
    "USA • Halloween": (10, 31),
    "USA • Valentine's Day": (2, 14),
    "USA • St. Patrick's Day": (3, 17),
    "USA • Veterans Day": (11, 11),
    "USA • Groundhog Day": (2, 2),
    "USA • Cinco de Mayo": (5, 5),
    "USA • Kwanzaa": (12, 26),
}


def get_next_festival_date(name):
    today = date.today()
    possible_dates = []

    # Fixed-date festivals
    if name in FIXED_DATES:
        month, day = FIXED_DATES[name]

        for year in range(today.year, today.year + 6):
            try:
                possible_dates.append(date(year, month, day))
            except ValueError:
                pass

    # US holidays calculated automatically
    calculated = us_festival_date(name, today.year)

    if calculated:
        possible_dates.append(calculated)

    if us_festival_date(name, today.year + 1):
        possible_dates.append(us_festival_date(name, today.year + 1))

    # Known dates for movable Indian festivals
    for year, festivals in MOVABLE_DATES.items():
        if name in festivals:
            month, day = festivals[name]
            possible_dates.append(date(year, month, day))

    future_dates = [d for d in possible_dates if d >= today]

    if not future_dates:
        return None

    return min(future_dates)


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("OMNI DELTA ENGINE v6.0")
root.geometry("1120x720")
root.minsize(950, 650)
root.configure(bg=BG)


# ============================================================
# STYLING
# ============================================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    fieldbackground=PANEL2,
    background=PANEL2,
    foreground=WHITE,
    arrowcolor=CYAN,
    bordercolor=BLUE,
    lightcolor=BLUE,
    darkcolor=BLUE
)

style.map(
    "TCombobox",
    fieldbackground=[("readonly", PANEL2)],
    foreground=[("readonly", WHITE)]
)


def make_label(parent, text, size=12, color=WHITE, bold=False):
    return tk.Label(
        parent,
        text=text,
        bg=parent.cget("bg"),
        fg=color,
        font=(FONT, size, "bold" if bold else "normal")
    )


def make_entry(parent, width=18):
    return tk.Entry(
        parent,
        width=width,
        bg=PANEL2,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=(FONT, 12),
        highlightthickness=1,
        highlightbackground=BLUE,
        highlightcolor=CYAN
    )


def make_button(parent, text, command, width=18):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        bg=BLUE,
        fg=WHITE,
        activebackground=CYAN,
        activeforeground=BG,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(FONT, 10, "bold"),
        padx=10,
        pady=9
    )


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=25, pady=(20, 10))

tk.Label(
    header,
    text="OMNI DELTA",
    bg=BG,
    fg=CYAN,
    font=(FONT, 29, "bold")
).pack()

tk.Label(
    header,
    text="COMPLIANT ENGINE  /  DATE & FESTIVAL SYSTEM",
    bg=BG,
    fg=MUTED,
    font=(FONT, 9, "bold")
).pack(pady=(2, 0))


# ============================================================
# MAIN TWO-COLUMN AREA
# ============================================================

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=25, pady=15)

main.grid_columnconfigure(0, weight=1)
main.grid_columnconfigure(1, weight=1)
main.grid_rowconfigure(0, weight=1)


# ============================================================
# LEFT PANEL - DATE CALCULATOR
# ============================================================

left = tk.Frame(
    main,
    bg=PANEL,
    highlightbackground=BLUE,
    highlightthickness=1
)
left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

make_label(
    left,
    "DATE DIFFERENCE CALCULATOR",
    15,
    CYAN,
    True
).pack(pady=(25, 8))

make_label(
    left,
    "Enter two dates to calculate the difference",
    9,
    MUTED
).pack(pady=(0, 20))


make_label(left, "START DATE  (YYYY-MM-DD)", 9, MUTED, True).pack()
entry_start = make_entry(left, 24)
entry_start.pack(pady=7)
entry_start.insert(0, date.today().strftime("%Y-%m-%d"))


make_label(left, "END DATE  (YYYY-MM-DD)", 9, MUTED, True).pack(pady=(15, 0))
entry_end = make_entry(left, 24)
entry_end.pack(pady=7)


result_box = tk.Frame(left, bg=PANEL2)
result_box.pack(fill="both", expand=True, padx=20, pady=20)

result_title = make_label(
    result_box,
    "CALCULATION RESULTS",
    11,
    CYAN,
    True
)
result_title.pack(pady=(15, 10))

result_label = tk.Label(
    result_box,
    text="Your results will appear here.",
    bg=PANEL2,
    fg=WHITE,
    font=(FONT, 12),
    justify="center",
    wraplength=400
)
result_label.pack(padx=15, pady=15, expand=True)


def calculate_between():
    try:
        start = datetime.strptime(
            entry_start.get().strip(), "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            entry_end.get().strip(), "%Y-%m-%d"
        ).date()

        difference = abs((end - start).days)

        weeks, remaining_days = divmod(difference, 7)
        hours = difference * 24
        minutes = hours * 60

        # Calculate calendar years, months and days
        earlier = min(start, end)
        later = max(start, end)

        years = later.year - earlier.year
        months = later.month - earlier.month
        days = later.day - earlier.day

        if days < 0:
            months -= 1

            previous_month = later.month - 1
            previous_year = later.year

            if previous_month == 0:
                previous_month = 12
                previous_year -= 1

            days += calendar.monthrange(
                previous_year, previous_month
            )[1]

        if months < 0:
            years -= 1
            months += 12

        result_label.config(
            text=(
                f"TOTAL DAYS\n{difference:,} days\n\n"
                f"WEEKS\n{weeks} weeks and {remaining_days} days\n\n"
                f"CALENDAR DIFFERENCE\n{years} years, {months} months, {days} days\n\n"
                f"TOTAL HOURS\n{hours:,} hours\n\n"
                f"TOTAL MINUTES\n{minutes:,} minutes"
            )
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Date",
            "Please enter both dates in YYYY-MM-DD format."
        )


make_button(
    left,
    "CALCULATE DIFFERENCE",
    calculate_between,
    25
).pack(pady=(0, 20))


# ============================================================
# RIGHT PANEL - FESTIVAL COUNTDOWN
# ============================================================

right = tk.Frame(
    main,
    bg=PANEL,
    highlightbackground=BLUE,
    highlightthickness=1
)
right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

make_label(
    right,
    "FESTIVAL COUNTDOWN",
    15,
    CYAN,
    True
).pack(pady=(25, 8))

make_label(
    right,
    "Select a festival to see its next countdown",
    9,
    MUTED
).pack(pady=(0, 20))


festival_var = tk.StringVar()

festival_dropdown = ttk.Combobox(
    right,
    textvariable=festival_var,
    values=FESTIVALS,
    state="readonly",
    width=43,
    font=(FONT, 10)
)
festival_dropdown.pack(padx=20, pady=5)


countdown_box = tk.Frame(right, bg=PANEL2)
countdown_box.pack(fill="both", expand=True, padx=20, pady=20)

make_label(
    countdown_box,
    "NEXT OCCURRENCE",
    10,
    CYAN,
    True
).pack(pady=(25, 10))


festival_title = tk.Label(
    countdown_box,
    text="SELECT A FESTIVAL",
    bg=PANEL2,
    fg=WHITE,
    font=(FONT, 13, "bold"),
    wraplength=390
)
festival_title.pack(pady=8)


days_label = tk.Label(
    countdown_box,
    text="---",
    bg=PANEL2,
    fg=CYAN,
    font=(FONT, 42, "bold")
)
days_label.pack(pady=(15, 0))


make_label(
    countdown_box,
    "DAYS",
    10,
    MUTED,
    True
).pack()


clock_label = tk.Label(
    countdown_box,
    text="00 : 00 : 00",
    bg=PANEL2,
    fg=WHITE,
    font=(FONT, 22, "bold")
)
clock_label.pack(pady=15)


target_label = tk.Label(
    countdown_box,
    text="Choose a festival above",
    bg=PANEL2,
    fg=MUTED,
    font=(FONT, 10)
)
target_label.pack(pady=5)


status_label = tk.Label(
    countdown_box,
    text="SYSTEM READY",
    bg=PANEL2,
    fg=GREEN,
    font=(FONT, 9, "bold")
)
status_label.pack(pady=(15, 5))


# ============================================================
# COUNTDOWN ENGINE
# ============================================================

selected_festival = None
selected_date = None


def select_festival(event=None):
    global selected_festival, selected_date

    selected_festival = festival_var.get()

    if not selected_festival:
        return

    selected_date = get_next_festival_date(selected_festival)

    festival_title.config(
        text=selected_festival.split(" • ", 1)[1]
    )

    if selected_date is None:
        days_label.config(text="N/A")
        clock_label.config(text="-- : -- : --")
        target_label.config(
            text="Date not currently available in the built-in calendar."
        )
        status_label.config(
            text="CALENDAR DATA UNAVAILABLE",
            fg="#FFB86B"
        )
        return

    target_label.config(
        text="Next occurrence: " + selected_date.strftime("%A, %d %B %Y")
    )

    status_label.config(
        text="COUNTDOWN ACTIVE",
        fg=GREEN
    )

    update_countdown()


def update_countdown():
    global selected_date

    if selected_date is not None:
        now = datetime.now()
        target = datetime.combine(selected_date, datetime.min.time())

        remaining = target - now

        if remaining.total_seconds() <= 0:
            days_label.config(text="0")
            clock_label.config(text="00 : 00 : 00")
            status_label.config(
                text="TODAY IS THE DAY!",
                fg=GREEN
            )
        else:
            total_seconds = int(remaining.total_seconds())

            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            days_label.config(text=f"{days:,}")

            clock_label.config(
                text=f"{hours:02d} : {minutes:02d} : {seconds:02d}"
            )

    root.after(1000, update_countdown)


festival_dropdown.bind(
    "<<ComboboxSelected>>",
    select_festival
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    root,
    text="OMNI DELTA ENGINE  •  VERSION 6.0  •  BLUE SYSTEM INTERFACE",
    bg=BG,
    fg=MUTED,
    font=(FONT, 8, "bold")
)
footer.pack(pady=(0, 15))


# ============================================================
# START APPLICATION
# ============================================================

festival_dropdown.current(0)
select_festival()

root.mainloop()
