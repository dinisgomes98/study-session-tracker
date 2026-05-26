class Session:

    def __init__(self, subject, date, time_spent, productivity) -> None:
        self.subject = subject
        self.date = date
        self.time_spent = time_spent
        self.productivity = productivity
  
    def __repr__(self):
        return (
            f"<Session: "
            f"{self.subject}, "
            f"{self.date.strftime('%d/%m/%Y')}, "
            f"{self.time_spent} min, "
            f"Productivity {self.productivity}/5>"
        )