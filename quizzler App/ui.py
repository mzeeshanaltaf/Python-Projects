from tkinter import *
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"
FONT = ("Arial", 20, "italic")

class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizler App")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Create a score label.
        self.score_label = Label(text=f"Score: {self.quiz.score}", bg=THEME_COLOR, fg="white", font=FONT)
        self.score_label.grid(row=0, column=2)

        # Create a canvas to display questions.
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Question will be \n displayed here",
            fill=THEME_COLOR,
            font=FONT)
        self.canvas.grid(row=1, column=0, columnspan=3, pady=50)

        # Create button for false answer.
        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image,
                                   highlightthickness=0,
                                   borderwidth=0,
                                   activebackground=THEME_COLOR,
                                   command=self.false_button_press)
        self.false_button.grid(row=2, column=0)

        # Create button for true answer.
        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image,
                                  highlightthickness=0,
                                  borderwidth=0,
                                  activebackground=THEME_COLOR,
                                  command=self.true_button_press)
        self.true_button.grid(row=2, column=2)

        self.get_next_question()

        self.window.mainloop()


    def get_next_question(self):
        self.canvas.config(bg="white")
        self.score_label.config(text=f"Score: {self.quiz.score}/{self.quiz.question_number}")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached end of the quiz")
            self.true_button.config(state=DISABLED)
            self.false_button.config(state=DISABLED)

    def false_button_press(self):
        self.give_feedback(self.quiz.check_answer('False'))

    def true_button_press(self):
        self.give_feedback(self.quiz.check_answer('True'))

    def give_feedback(self, is_right: bool):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000,self.get_next_question)







