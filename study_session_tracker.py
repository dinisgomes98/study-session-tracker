from session import Session
from datetime import datetime, timedelta


def main():
    print("Running Study Session Tracker!")

    session_file_path = "sessions.csv"
    subject_file_path = "subjects.csv"


    option = 0

    while option != 5:
        print("*** Study Session Tracker ***")
        print("1) Add session")
        print("2) Add new subject")
        print("3) Check this week performance")
        print("4) Check overall performance")
        print("5) Quit")

        try:
            option = int(input("Choose an option >>> "))
        except ValueError:
            print("Please enter a number from 1 to 5")
            continue

        if option == 1:
            #get user session input
            session = get_user_session(subject_file_path)

            #save session
            save_session_to_file(session, session_file_path)
                    
        
        elif option == 2:
            #get subject
            subject = input("Enter new subject: ")

            #save subject
            save_subject_to_file(subject, subject_file_path)
            
                                    
        elif option == 3:
            #get week
            week_sessions = get_week_sessions(session_file_path)

            #check performance
            get_performance(week_sessions)



        
        elif option == 4:
            #get all sessions
            all_sessions = get_all_sessions(session_file_path)

            #check performance
            get_performance(all_sessions)

            
    

        elif option == 5:
            print("Quitting program")

        else:
            print("Invalid option. Please choose from 1 to 5")

    print("Program closed!")


def get_user_session(subject_file_path):

    #get subject
    try:
        with open(subject_file_path, "r") as f:
            subjects = [line.strip() for line in f]
    except FileNotFoundError:
        subjects = []

    subjects.append("New Subject")

    while True:
        print("Select a subject: ")
        
        for i, subject_name in enumerate(subjects):
            print(f"{i+1}. {subject_name}")

        value_range = f"[1 - {len(subjects)}]"
        
        try:
            selected_index = int(input(f"Enter subject number {value_range}: ")) - 1
        except ValueError:
            print("Please enter a valid number")
            continue


        if selected_index == len(subjects) -1:
            subject_category = input("Enter new subject: ")
            save_subject_to_file(subject_category, subject_file_path)
            break

        elif selected_index in range(len(subjects)):
            subject_category = subjects[selected_index]
            break

        else:
            print("Invalid subject. Please try again!")
        
    #get date
    while True:
        date_input = input("Enter date (DD/MM/YYYY): ")

        try:
            valid_date = datetime.strptime(date_input, "%d/%m/%Y")
            break
        except ValueError:
            print("Please enter a valid date")


    #get time    
    while True:
        try: 
            time = int(input("Enter time spent in minutes: "))
            break
        except ValueError:
            print("Please enter a valid time spent")

    #get productivity
    while True:
        try: 
            productivity_note = int(input("Enter how much productive was the session(from 1-5): "))

            if productivity_note in range(1,6):
                break
            else:
                print("Please enter a number from 1 to 5")

        except ValueError:
            print("Please enter a valid number")
            

    new_session = Session(subject = subject_category, date= valid_date, time_spent= time, productivity=productivity_note)

    return new_session


def save_session_to_file(session: Session, session_file_path):
    with open(session_file_path, "a") as f:
        f.write(
            f"{session.subject},{session.date.strftime('%d/%m/%Y')},{session.time_spent},{session.productivity}\n"
        )

def save_subject_to_file(subject, subject_file_path):
    with open(subject_file_path, "a") as f:
        f.write(f"{subject}\n")


def get_week_sessions(session_file_path):
    today = datetime.today()

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    sessions_of_week = []

    try:
        with open(session_file_path, "r") as f:

            for line in f:

                subject, date, time_spent, productivity = line.strip().split(",")

                session_date = datetime.strptime(date, "%d/%m/%Y")

                session = Session(
                    subject=subject,
                    date=session_date,
                    time_spent=int(time_spent),
                    productivity=int(productivity)
                )

                if start_of_week.date() <= session.date.date() <= end_of_week.date():
                    sessions_of_week.append(session)

    except FileNotFoundError:
        return []
    

    return sessions_of_week

def get_all_sessions(session_file_path):

    sessions = []

    try:
        with open(session_file_path, "r") as f:

            for line in f:

                subject, date, time_spent, productivity = line.strip().split(",")

                session_date = datetime.strptime(date, "%d/%m/%Y")

                session = Session(
                    subject=subject,
                    date=session_date,
                    time_spent=int(time_spent),
                    productivity=int(productivity)
                )

                sessions.append(session)

    except FileNotFoundError:
        return []

    return sessions


def get_performance(sessions):

    if not sessions:
        print("No sessions found")
        return

    time_spent = 0
    total_productivity = 0

    for session in sessions:
        time_spent += session.time_spent
        total_productivity += session.productivity

    avg_productivity = total_productivity / len(sessions)

    time_by_subject = {}

    for session in sessions:
        key = session.subject

        if key in time_by_subject:
            time_by_subject[key] += session.time_spent
        else:
            time_by_subject[key] = session.time_spent
    
    most_time_subject = max(time_by_subject, key=time_by_subject.get)

    best_session = sessions[0]

    for session in sessions[1:]:

        if session.productivity > best_session.productivity:
            best_session = session

        elif (session.productivity == best_session.productivity and session.time_spent < best_session.time_spent):
            best_session = session


    print(f"Amount of time spent: {time_spent} min\n")
    print(f"Productivity note: {avg_productivity:.2f}\n")
    print(f"Subject most studied: {most_time_subject}\n")
    print(f"Most productive session: {best_session}\n")


if __name__ == "__main__":
    main()